#!/usr/bin/env python3
"""
scrape-reviews.py
-----------------
Scrapes reviews from Yelp and Google Maps using Playwright, with automated
thematic sentiment analysis, polarity scoring, and keyword clustering.

Supports:
  - Custom Yelp/Google URLs & search query terms
  - Star rating filtering
  - Automated sentiment analysis (-1.0 to +1.0 polarity score per review)
  - Thematic keyword clustering:
      * Common Praises: painless, compassionate, fast settlement, responsive,
        knowledgeable, friendly staff, transparent, highly recommend.
      * Common Complaints / Red Flags: wait time, billing dispute, unresponsive,
        hidden fee, rushed, rude, overcharged, cancelled appointment.
  - Formatted JSON & CSV export with top-level sentiment summary
  - Standalone review file analysis without active browser scraping (--input-file)

Requirements:
  pip install playwright
  playwright install chromium

Usage:
  python3 scripts/scrape-reviews.py --source google --google-url "https://www.google.com/maps/search/..."
  python3 scripts/scrape-reviews.py --source yelp --yelp-url "https://www.yelp.com/biz/example"
  python3 scripts/scrape-reviews.py --source all --output reviews/export --sentiment-summary
  python3 scripts/scrape-reviews.py --input-file reviews/export.json --sentiment-summary
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import random
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Review:
    source: str   # "yelp" | "google"
    author: str
    rating: int   # 1-5
    date: str
    text: str
    url: str = ""
    sentiment_score: float = 0.0
    praises: list[str] = field(default_factory=list)
    complaints: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Sentiment & Thematic Keyword Clustering Definitions
# ---------------------------------------------------------------------------

PRAISE_CLUSTERS: dict[str, list[str]] = {
    "painless": [
        r"\bpainless\b",
        r"\bpain[\s-]?free\b",
        r"\beasy process\b",
        r"\bsmooth process\b",
        r"\bseamless\b",
        r"\beffortless\b",
        r"\bhassle[\s-]?free\b",
        r"\bstress[\s-]?free\b",
        r"\bno stress\b",
    ],
    "compassionate": [
        r"\bcompassion(?:ate)?\b",
        r"\bcaring\b",
        r"\bempath(?:y|etic)\b",
        r"\bkind(?:ness|ly)?\b",
        r"\bthoughtful\b",
        r"\bunderstanding\b",
        r"\bsupportive\b",
        r"\bheartfelt\b",
    ],
    "fast settlement": [
        r"\bfast settlement\b",
        r"\bquick settlement\b",
        r"\bsettled quickly\b",
        r"\bsettled fast\b",
        r"\bspeedy settlement\b",
        r"\bfast resolution\b",
        r"\bquick payout\b",
        r"\bfast turnaround\b",
        r"\bresolved quickly\b",
        r"\bhandled quickly\b",
        r"\bquick check\b",
        r"\bfast check\b",
    ],
    "responsive": [
        r"\bresponsive(?:ness)?\b",
        r"\bquick to respond\b",
        r"\balways answer(?:ed|s)?\b",
        r"\banswered right away\b",
        r"\bprompt(?:ly)?\b",
        r"\bkept (?:me|us) informed\b",
        r"\balways called back\b",
        r"\bgreat communication\b",
        r"\bexcellent communication\b",
        r"\bfast reply\b",
        r"\breachable\b",
    ],
    "knowledgeable": [
        r"\bknowledgeable\b",
        r"\bexpert(?:ise)?\b",
        r"\bprofessional(?:ism)?\b",
        r"\bexperienced\b",
        r"\bcompetent\b",
        r"\bskilled\b",
        r"\bthorough\b",
        r"\bmasterful\b",
        r"\bknows (?:his|their|her) stuff\b",
        r"\bwell informed\b",
    ],
    "friendly staff": [
        r"\bfriendly staff\b",
        r"\bcourteous staff\b",
        r"\bwonderful staff\b",
        r"\bgreat team\b",
        r"\bhelpful staff\b",
        r"\bcourteous\b",
        r"\bwelcoming\b",
        r"\bwarm staff\b",
        r"\bpolite staff\b",
        r"\bamazing staff\b",
        r"\bfriendly\b",
        r"\bwelcoming team\b",
    ],
    "transparent": [
        r"\btransparent\b",
        r"\btransparency\b",
        r"\bhonest(?:y)?\b",
        r"\bno surprises\b",
        r"\bclear explanation\b",
        r"\bexplained everything clearly\b",
        r"\bupfront\b",
        r"\bstraightforward\b",
        r"\btrustworthy\b",
        r"\bkept (?:his|their|her) word\b",
    ],
    "highly recommend": [
        r"\b(?:highly|strongly|definitely)?\s*recommend(?:ed|ing)?\b",
        r"\bcannot recommend enough\b",
        r"\bwould recommend\b",
        r"\b10/10\b",
        r"\btop notch\b",
        r"\bfive stars\b",
        r"\b5 stars?\b",
        r"\bbest lawyer\b",
        r"\bbest attorney\b",
        r"\bbest law firm\b",
    ],
}

COMPLAINT_CLUSTERS: dict[str, list[str]] = {
    "wait time": [
        r"\bwait(?:ing)? time\b",
        r"\blong wait\b",
        r"\bwaited for hours\b",
        r"\bwaited forever\b",
        r"\bdelays?\b",
        r"\bdelayed\b",
        r"\btook forever\b",
        r"\bslow process\b",
        r"\btook months with no update\b",
        r"\bsitting in the waiting room\b",
        r"\binterminable wait\b",
    ],
    "billing dispute": [
        r"\bbilling dispute\b",
        r"\bbilling issue\b",
        r"\bbilling error\b",
        r"\bunexpected bill\b",
        r"\bdisputed charge\b",
        r"\bdisputed billing\b",
        r"\bfee dispute\b",
        r"\baccounting error\b",
        r"\bbilling problem\b",
        r"\bsurprise bill\b",
    ],
    "unresponsive": [
        r"\bunresponsive\b",
        r"\bnever answered(?: my calls)?\b",
        r"\bnever called back\b",
        r"\bno response\b",
        r"\bignored (?:my|our) (?:calls|emails|messages)\b",
        r"\bhard to reach\b",
        r"\bpoor communication\b",
        r"\black of communication\b",
        r"\bghosted\b",
        r"\bnever reached out\b",
        r"\bimpossible to reach\b",
    ],
    "hidden fee": [
        r"\bhidden fees?\b",
        r"\bhidden costs?\b",
        r"\bextra charges?\b",
        r"\bsurprise fees?\b",
        r"\bsurprise charges?\b",
        r"\bunclear pricing\b",
        r"\bundisclosed fees?\b",
        r"\bnickel and dime\b",
    ],
    "rushed": [
        r"\brushed\b",
        r"\bfelt rushed\b",
        r"\bhurried\b",
        r"\bin a rush\b",
        r"\bdismissive\b",
        r"\bno time for me\b",
        r"\bspent two minutes\b",
        r"\bbrushed off\b",
        r"\btoo quick to dismiss\b",
    ],
    "rude": [
        r"\brude(?:ness)?\b",
        r"\bdisrespectful\b",
        r"\bcondescending\b",
        r"\barrogant\b",
        r"\battitude\b",
        r"\bhostile\b",
        r"\bunfriendly\b",
        r"\binsulting\b",
        r"\bbad attitude\b",
        r"\bimpatient\b",
    ],
    "overcharged": [
        r"\bovercharg(?:ed|ing)\b",
        r"\brip[\s-]?off\b",
        r"\btoo expensive\b",
        r"\bprice gouging\b",
        r"\bexorbitant\b",
        r"\bhighway robbery\b",
        r"\bgrossly overpriced\b",
        r"\boutrageous fees?\b",
    ],
    "cancelled appointment": [
        r"\bcancell?ed appointment\b",
        r"\bcancell?ed last minute\b",
        r"\bno show\b",
        r"\brescheduled multiple times\b",
        r"\bcancell?ed on me\b",
        r"\bappointment cancellation\b",
    ],
}

POSITIVE_LEXICON: dict[str, float] = {
    "great": 0.8, "excellent": 0.9, "amazing": 0.95, "wonderful": 0.9, "fantastic": 0.95,
    "best": 1.0, "awesome": 0.9, "good": 0.5, "helpful": 0.7, "caring": 0.8,
    "compassionate": 0.85, "painless": 0.8, "responsive": 0.85, "prompt": 0.75,
    "professional": 0.8, "knowledgeable": 0.85, "friendly": 0.75, "honest": 0.85,
    "transparent": 0.8, "recommend": 0.85, "thorough": 0.7, "fast": 0.7,
    "settlement": 0.5, "easy": 0.6, "smooth": 0.7, "satisfied": 0.8, "pleased": 0.75,
    "love": 0.9, "perfect": 1.0, "exceptional": 0.95, "superb": 0.9, "stellar": 0.9,
    "fair": 0.6, "trustworthy": 0.85, "courteous": 0.7, "attentive": 0.75,
}

NEGATIVE_LEXICON: dict[str, float] = {
    "terrible": -0.95, "horrible": -0.95, "awful": -0.9, "worst": -1.0, "bad": -0.6,
    "rude": -0.85, "unresponsive": -0.9, "overcharged": -0.9, "unprofessional": -0.85,
    "rushed": -0.7, "hidden": -0.6, "fee": -0.3, "dispute": -0.7, "delayed": -0.6,
    "slow": -0.5, "disappointed": -0.8, "disappointing": -0.8, "waste": -0.85, "scam": -1.0,
    "liar": -1.0, "unhelpful": -0.75, "poor": -0.7, "nightmare": -0.95, "arrogant": -0.85,
    "mistake": -0.6, "regret": -0.8, "frustrated": -0.75, "painful": -0.8, "disaster": -0.95,
    "incompetent": -0.9, "hostile": -0.85, "dishonest": -0.95, "ignored": -0.8, "ridiculous": -0.7,
}


USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]


# ---------------------------------------------------------------------------
# Lazy Playwright Loader
# ---------------------------------------------------------------------------

def require_playwright():
    try:
        from playwright.async_api import async_playwright
        return async_playwright
    except ImportError:
        print("❌  Playwright not installed. Run:")
        print("    pip install playwright && playwright install chromium")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def rdelay(lo: int = 800, hi: int = 2400) -> None:
    await asyncio.sleep(random.uniform(lo / 1000, hi / 1000))


def clean(text: str) -> str:
    return " ".join(text.split()).strip()


def is_negated(text: str, match_start: int) -> bool:
    """
    Checks if a pattern match at match_start is preceded by a negation within
    the same clause or sentence fragment (bounded by punctuation or conjunctions).
    """
    window_start = max(0, match_start - 40)
    preceding = text[window_start:match_start]
    parts = re.split(r"[,;:.!?\n]|\b(?:and|but|however|although)\b", preceding)
    clause = parts[-1] if parts else preceding
    return bool(re.search(
        r"\b(?:no|not|never|without|zero|none|free of|hardly|barely|don't|didnt|didn't|dont|cannot|can't|wouldnt|wouldn't|neither|nor)\b",
        clause,
        re.IGNORECASE
    ))


def analyze_review_sentiment(text: str, rating: int) -> tuple[float, list[str], list[str]]:
    """
    Performs thematic keyword clustering and computes polarity score (-1.0 to +1.0)
    combining star rating and text sentiment heuristics.
    """
    text_lower = text.lower()

    # 1. Cluster Praises
    praises: set[str] = set()
    for theme, patterns in PRAISE_CLUSTERS.items():
        for pat in patterns:
            for m in re.finditer(pat, text_lower, re.IGNORECASE):
                if not is_negated(text_lower, m.start()):
                    praises.add(theme)
                    break

    # 2. Cluster Complaints
    complaints: set[str] = set()
    for theme, patterns in COMPLAINT_CLUSTERS.items():
        for pat in patterns:
            for m in re.finditer(pat, text_lower, re.IGNORECASE):
                if is_negated(text_lower, m.start()):
                    # Negated complaint -> e.g. "no hidden fees" implies transparency
                    if theme == "hidden fee":
                        praises.add("transparent")
                else:
                    complaints.add(theme)
                    break

    # Cross-negation checks
    if re.search(r"\b(?:not|never|hardly)\s+(?:responsive|answering)\b", text_lower):
        complaints.add("unresponsive")
        praises.discard("responsive")
    if re.search(r"\b(?:not|never|hardly)\s+friendly\b", text_lower):
        complaints.add("rude")
        praises.discard("friendly staff")
    if re.search(r"\b(?:would not|don't|dont|do not|never)\s+recommend\b", text_lower):
        praises.discard("highly recommend")

    # 3. Text Polarity Heuristics
    words = re.findall(r"\b[\w'-]+\b", text_lower)
    word_scores: list[float] = []

    for i, w in enumerate(words):
        score = 0.0
        if w in POSITIVE_LEXICON:
            score = POSITIVE_LEXICON[w]
        elif w in NEGATIVE_LEXICON:
            score = NEGATIVE_LEXICON[w]
        else:
            continue

        prec = words[max(0, i - 3):i]
        prec_str = " ".join(prec)
        neg = bool(re.search(r"\b(?:no|not|never|without|hardly|barely|don't|didnt|didn't|dont|cannot|can't)\b", prec_str))
        intensified = bool(re.search(r"\b(?:very|extremely|highly|absolutely|truly|so|super|really|incredibly)\b", prec_str))
        diminished = bool(re.search(r"\b(?:somewhat|slightly|a bit)\b", prec_str))

        if neg:
            score = -score * 0.8
        elif intensified:
            score = min(1.0, max(-1.0, score * 1.3))
        elif diminished:
            score = score * 0.6

        word_scores.append(score)

    if word_scores:
        text_polarity = sum(word_scores) / (len(word_scores) ** 0.5 + 0.5)
        text_polarity = max(-1.0, min(1.0, text_polarity))
    else:
        text_polarity = 0.0

    # Rating Polarity
    has_rating = 1 <= rating <= 5
    if has_rating:
        rating_polarity = (rating - 3.0) / 2.0  # 1 -> -1.0, 3 -> 0.0, 5 -> +1.0
        if word_scores:
            final_score = 0.55 * rating_polarity + 0.45 * text_polarity
        else:
            final_score = rating_polarity
    else:
        final_score = text_polarity

    final_score = round(max(-1.0, min(1.0, final_score)), 2)
    return final_score, sorted(list(praises)), sorted(list(complaints))


def compute_sentiment_summary(reviews: list[Review]) -> dict[str, Any]:
    """
    Aggregates frequency counts of praises and complaints, and computes the average sentiment score.
    """
    if not reviews:
        return {
            "praises": [],
            "complaints": [],
            "average_sentiment": 0.0,
        }

    total_sentiment = sum(r.sentiment_score for r in reviews)
    avg_sentiment = round(total_sentiment / len(reviews), 2)

    praise_counts: Counter[str] = Counter()
    complaint_counts: Counter[str] = Counter()

    for r in reviews:
        for p in r.praises:
            praise_counts[p] += 1
        for c in r.complaints:
            complaint_counts[c] += 1

    sorted_praises = [
        {"theme": theme, "keyword": theme, "count": count}
        for theme, count in praise_counts.most_common()
    ]
    sorted_complaints = [
        {"theme": theme, "keyword": theme, "count": count}
        for theme, count in complaint_counts.most_common()
    ]

    return {
        "praises": sorted_praises,
        "complaints": sorted_complaints,
        "average_sentiment": float(avg_sentiment),
    }


def print_sentiment_summary(summary_data: dict[str, Any], total_reviews: int) -> None:
    """
    Prints top 5 praises and top 5 complaints with frequency counts to the terminal.
    """
    avg_score = summary_data.get("average_sentiment", 0.0)
    praises = summary_data.get("praises", [])
    complaints = summary_data.get("complaints", [])

    print(f"\n{'─'*54}")
    print("  Thematic Sentiment Analysis & Keyword Clustering")
    print(f"{'─'*54}")
    print(f"  Reviews Analyzed   : {total_reviews}")
    print(f"  Average Sentiment  : {avg_score:+.2f}  (-1.00 to +1.00)")
    print()
    print("  Top 5 Praises:")
    if praises:
        for i, item in enumerate(praises[:5], 1):
            print(f"    {i}. {item['theme']} ({item['count']})")
    else:
        print("    (None detected)")

    print()
    print("  Top 5 Complaints / Red Flags:")
    if complaints:
        for i, item in enumerate(complaints[:5], 1):
            print(f"    {i}. {item['theme']} ({item['count']})")
    else:
        print("    (None detected)")
    print(f"{'─'*54}\n")


# ---------------------------------------------------------------------------
# Yelp scraper
# ---------------------------------------------------------------------------

async def scrape_yelp(
    ctx: Any,
    yelp_url: str,
    max_pages: int = 20,
    min_rating: int = 5,
) -> list[Review]:
    if not yelp_url:
        print("   ⚠️  No Yelp URL provided. Skipping Yelp scrape.")
        return []

    reviews: list[Review] = []
    page = await ctx.new_page()
    url = yelp_url

    print(f"\n🔍  Scraping Yelp ({min_rating}★ and above)…")

    for pnum in range(max_pages):
        print(f"   Page {pnum + 1}: {url}")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=40_000)
            await rdelay(1500, 3000)
        except Exception as e:
            print(f"   ⚠️  Failed to load {url}: {e}")
            break

        # Dismiss popups / cookie banners silently
        for sel in [
            "button[data-testid='yelp-close-btn']",
            "button[aria-label='Close']",
            "#onetrust-accept-btn-handler",
        ]:
            try:
                btn = page.locator(sel).first
                if await btn.is_visible(timeout=1500):
                    await btn.click()
                    await rdelay(300, 600)
            except Exception:
                pass

        # Review cards
        cards = await page.query_selector_all(
            '[data-testid="review-body"], '
            'li[data-review-id], '
            'section[class*="review-list"] li'
        )
        if not cards:
            cards = await page.query_selector_all('li[class*="margin-b"]')

        before = len(reviews)

        for card in cards:
            try:
                star_el = await card.query_selector('[aria-label*="star rating"]')
                rating = 0
                if star_el:
                    aria = await star_el.get_attribute("aria-label") or ""
                    m = re.search(r"(\d)", aria)
                    if m:
                        rating = int(m.group(1))

                if rating < min_rating:
                    continue

                a_el = await card.query_selector(
                    '[class*="user-display-name"], a[href*="/user_details"]'
                )
                author = clean(await a_el.inner_text()) if a_el else "Anonymous"

                d_el = await card.query_selector(
                    'span[class*="date"], time, [class*="review-date"]'
                )
                date_str = clean(await d_el.inner_text()) if d_el else ""

                t_el = await card.query_selector(
                    'p[class*="comment"], [class*="review-content"] p, p[lang]'
                )
                if not t_el:
                    t_el = await card.query_selector("p")
                text = clean(await t_el.inner_text()) if t_el else ""

                if text:
                    reviews.append(Review(
                        source="yelp",
                        author=author,
                        rating=rating,
                        date=date_str,
                        text=text,
                        url=url,
                    ))
                    print(f"      ★  {author[:30]:<30}  {date_str[:25]}")

            except Exception:
                pass

        if len(reviews) == before:
            print("   ℹ️  No matching reviews found on this page.")

        # Next page
        next_btn = page.locator('a[aria-label*="Next"]').first
        if await next_btn.count() == 0:
            next_btn = page.locator('[class*="pagination"] a:has-text("Next")').first

        if await next_btn.count() > 0 and await next_btn.is_enabled():
            href = await next_btn.get_attribute("href") or ""
            if href:
                url = href if href.startswith("http") else f"https://www.yelp.com{href}"
                await rdelay(1500, 3000)
                continue

        print("   ℹ️  No more Yelp pages.")
        break

    await page.close()
    print(f"   ✅  {len(reviews)} Yelp reviews collected.")
    return reviews


# ---------------------------------------------------------------------------
# Google Maps scraper
# ---------------------------------------------------------------------------

async def scrape_google(
    ctx: Any,
    google_url: str,
    max_scrolls: int = 60,
    min_rating: int = 5,
) -> list[Review]:
    if not google_url:
        print("   ⚠️  No Google Maps URL/query provided. Skipping Google scrape.")
        return []

    reviews: list[Review] = []
    page = await ctx.new_page()
    seen: set[str] = set()

    target_url = (
        google_url
        if google_url.startswith("http")
        else f"https://www.google.com/maps/search/{google_url.replace(' ', '+')}"
    )

    print(f"\n🔍  Scraping Google Maps reviews ({min_rating}★ and above)…")
    try:
        await page.goto(target_url, wait_until="domcontentloaded", timeout=40_000)
        await rdelay(2500, 4000)
    except Exception as e:
        print(f"   ⚠️  Failed to load {target_url}: {e}")
        await page.close()
        return []

    # If we landed on search results list, click first item
    try:
        first = page.locator('a[data-cid], [class*="hfpxzc"]').first
        if await first.count() > 0:
            await first.click()
            await rdelay(2000, 3500)
    except Exception:
        pass

    # Click "Reviews" tab
    for sel in [
        'button[aria-label*="Reviews"]',
        '[data-tab-index="1"]',
        'button:has-text("Reviews")',
    ]:
        try:
            tab = page.locator(sel).first
            if await tab.count() > 0:
                await tab.click()
                await rdelay(1500, 2500)
                break
        except Exception:
            pass

    # Try to click 5-star filter chip if min_rating == 5
    if min_rating >= 5:
        try:
            chip = page.locator('button[aria-label*="5 star"], [data-rating="5"]').first
            if await chip.count() > 0:
                await chip.click()
                await rdelay(1500, 2500)
                print("   ✅  Applied 5★ filter chip.")
        except Exception:
            pass

    no_new = 0
    last_count = 0

    for _ in range(max_scrolls):
        cards = await page.query_selector_all(
            '[data-review-id], '
            'div[class*="jJc9Ad"], '
            'div[class*="WMbnJf"]'
        )

        for card in cards:
            try:
                r_el = await card.query_selector('[aria-label*="star"], [aria-label*="Rated"]')
                rating = 0
                if r_el:
                    aria = await r_el.get_attribute("aria-label") or ""
                    m = re.search(r"(\d+(?:\.\d+)?)", aria)
                    if m:
                        rating = round(float(m.group(1)))

                if rating < min_rating:
                    continue

                try:
                    more = await card.query_selector(
                        'button[aria-label*="See more"], button.w8nwRe'
                    )
                    if more:
                        await more.click()
                        await asyncio.sleep(0.2)
                except Exception:
                    pass

                t_el = await card.query_selector(
                    '[class*="wiI7pd"], span[jsname], [class*="review-full-text"]'
                )
                text = clean(await t_el.inner_text()) if t_el else ""
                if not text or text in seen:
                    continue
                seen.add(text)

                a_el = await card.query_selector(
                    '[class*="d4r55"], [class*="Vpc5Fe"], .WNxzHc a'
                )
                author = clean(await a_el.inner_text()) if a_el else "Anonymous"

                d_el = await card.query_selector('[class*="rsqaWe"], [class*="xRkPPb"]')
                date_str = clean(await d_el.inner_text()) if d_el else ""

                reviews.append(Review(
                    source="google",
                    author=author,
                    rating=rating,
                    date=date_str,
                    text=text,
                    url=page.url,
                ))
                print(f"      ★  {author[:30]:<30}  {date_str[:25]}")

            except Exception:
                pass

        if len(reviews) == last_count:
            no_new += 1
            if no_new >= 6:
                print("   ℹ️  No new reviews after 6 scrolls — stopping.")
                break
        else:
            no_new = 0
            last_count = len(reviews)

        scrolled = False
        for panel_sel in [
            '[class*="m6QErb"][class*="DxyBCb"]',
            'div[role="main"] div[tabindex="-1"]',
            '[jsaction*="pane.reviewlist"]',
        ]:
            try:
                panel = page.locator(panel_sel).first
                if await panel.count() > 0:
                    await panel.evaluate("el => el.scrollBy(0, 1000)")
                    scrolled = True
                    break
            except Exception:
                pass

        if not scrolled:
            await page.mouse.wheel(0, 1000)

        await rdelay(700, 1400)

    await page.close()
    print(f"   ✅  {len(reviews)} Google reviews collected.")
    return reviews


# ---------------------------------------------------------------------------
# Output & Summary
# ---------------------------------------------------------------------------

def save_json(
    reviews: list[Review],
    path: Path,
    sentiment_summary_data: dict[str, Any] | None = None,
) -> None:
    out: dict[str, Any] = {
        "generated": datetime.now().isoformat(),
        "total": len(reviews),
    }
    if sentiment_summary_data is not None:
        out["sentiment_summary"] = sentiment_summary_data
    out["reviews"] = [asdict(r) for r in reviews]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n💾  JSON  → {path}")


def save_csv(reviews: list[Review], path: Path) -> None:
    fields = [
        "source", "author", "rating", "date", "text", "url",
        "sentiment_score", "praises", "complaints"
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in reviews:
            row = asdict(r)
            row["praises"] = "; ".join(r.praises)
            row["complaints"] = "; ".join(r.complaints)
            w.writerow(row)
    print(f"💾  CSV   → {path}")


def summary(reviews: list[Review]) -> None:
    yelp   = [r for r in reviews if r.source == "yelp"]
    google = [r for r in reviews if r.source == "google"]
    print(f"\n{'─'*48}")
    print(f"  Total reviews    : {len(reviews)}")
    print(f"  Yelp             : {len(yelp)}")
    print(f"  Google           : {len(google)}")
    print(f"{'─'*48}\n")


def load_reviews_file(path: Path) -> list[Review]:
    """Loads existing reviews from a JSON or CSV file."""
    if not path.exists():
        print(f"❌  Input file does not exist: {path}")
        sys.exit(1)

    reviews: list[Review] = []
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        items = data.get("reviews", data) if isinstance(data, dict) else data
        for item in items:
            reviews.append(Review(
                source=item.get("source", "unknown"),
                author=item.get("author", "Anonymous"),
                rating=int(item.get("rating", 5)),
                date=item.get("date", ""),
                text=item.get("text", ""),
                url=item.get("url", ""),
            ))
    elif path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                reviews.append(Review(
                    source=row.get("source", "unknown"),
                    author=row.get("author", "Anonymous"),
                    rating=int(row.get("rating", 5) or 5),
                    date=row.get("date", ""),
                    text=row.get("text", ""),
                    url=row.get("url", ""),
                ))
    else:
        print(f"❌  Unsupported input file extension: {path.suffix} (use .json or .csv)")
        sys.exit(1)

    print(f"📂  Loaded {len(reviews)} reviews from {path}")
    return reviews


# ---------------------------------------------------------------------------
# Main Routine
# ---------------------------------------------------------------------------

async def main(
    source: str,
    output: str,
    fmt: str,
    headed: bool,
    yelp_url: str,
    google_url: str,
    min_rating: int,
    analyze_sentiment: bool,
    sentiment_summary_flag: bool,
    input_file: str | None,
) -> None:
    out = Path(output)
    reviews: list[Review] = []

    if input_file:
        reviews = load_reviews_file(Path(input_file))
    else:
        async_playwright = require_playwright()
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(
                headless=not headed,
                args=["--disable-blink-features=AutomationControlled"],
            )
            ctx = await browser.new_context(
                user_agent=random.choice(USER_AGENTS),
                viewport={"width": 1280, "height": 900},
                locale="en-US",
            )
            await ctx.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
            )

            if source in ("yelp", "all"):
                reviews += await scrape_yelp(ctx, yelp_url, min_rating=min_rating)

            if source in ("google", "all"):
                reviews += await scrape_google(ctx, google_url, min_rating=min_rating)

            await browser.close()

    # Sentiment Analysis & Clustering
    sentiment_data: dict[str, Any] | None = None
    if analyze_sentiment:
        for r in reviews:
            r.sentiment_score, r.praises, r.complaints = analyze_review_sentiment(r.text, r.rating)
        sentiment_data = compute_sentiment_summary(reviews)

    # Basic Counts Summary
    summary(reviews)

    # Thematic Sentiment Summary if requested
    if sentiment_summary_flag and sentiment_data:
        print_sentiment_summary(sentiment_data, len(reviews))

    # Save Output
    if fmt in ("json", "both"):
        save_json(reviews, out.with_suffix(".json"), sentiment_summary_data=sentiment_data)
    if fmt in ("csv", "both"):
        save_csv(reviews, out.with_suffix(".csv"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape customer reviews from Yelp and Google Maps with automated thematic sentiment analysis & keyword clustering."
    )
    parser.add_argument(
        "--source",
        choices=["yelp", "google", "all"],
        default="all",
        help="Platform to scrape (default: all)",
    )
    parser.add_argument(
        "--yelp-url",
        default="https://www.yelp.com/biz/the-law-offices-of-jacob-emrani-los-angeles-2",
        help="Yelp business URL to scrape",
    )
    parser.add_argument(
        "--google-url",
        default="The Law Offices of Jacob Emrani Los Angeles",
        help="Google Maps business search query or direct URL",
    )
    parser.add_argument(
        "--min-rating",
        type=int,
        default=5,
        help="Minimum star rating to include (1-5, default: 5)",
    )
    parser.add_argument(
        "--output",
        default="reviews/scraped-reviews",
        help="Output path without extension (default: reviews/scraped-reviews)",
    )
    parser.add_argument(
        "--format",
        dest="fmt",
        choices=["json", "csv", "both"],
        default="both",
        help="Output format (default: both)",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Show the browser window (useful for debugging)",
    )
    parser.add_argument(
        "--analyze-sentiment",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable automated thematic sentiment analysis and keyword clustering (default: True)",
    )
    parser.add_argument(
        "--sentiment-summary",
        action="store_true",
        default=False,
        help="Print top 5 praises and top 5 complaints with frequency counts to console",
    )
    parser.add_argument(
        "--input-file",
        type=str,
        default=None,
        help="Optional path to existing JSON or CSV reviews file to analyze sentiment without scraping",
    )
    args = parser.parse_args()
    asyncio.run(
        main(
            args.source,
            args.output,
            args.fmt,
            args.headed,
            args.yelp_url,
            args.google_url,
            args.min_rating,
            args.analyze_sentiment,
            args.sentiment_summary,
            args.input_file,
        )
    )
