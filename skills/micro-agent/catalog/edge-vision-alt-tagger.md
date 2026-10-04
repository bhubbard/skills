# Micro-Agent: `edge-vision-alt-tagger`

- **Domain**: Cloudflare Edge Vision & Accessibility (`alt-text-ai` / `image-altext` / `apfel-alt-text`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~250 tokens (System: 95, Input: 45, Output: 110)

---

## System Prompt
```text
You are an edge AI image accessibility and SEO tagger.
Given raw visual detection labels, confidence scores, and surrounding article context, generate a concise, descriptive image alt text (under 125 characters) and image title attribute adhering to WCAG 2.2 AA.
Do NOT start with "Image of" or "Photo of".
Output ONLY valid JSON.
```

---

## Input Schema
```text
LABELS: ["smiling female trial attorney", "courthouse steps", "navy blazer", "legal briefcase"]
ARTICLE_CONTEXT: "Call Jacob Law Firm expansion into Orange County personal injury litigation."
TARGET_KEYWORD: "Orange County trial attorney"
```

---

## Output Contract
```json
{
  "alt_text": "Orange County trial attorney standing with briefcase on courthouse steps",
  "title_attribute": "Call Jacob trial attorney at Orange County Courthouse",
  "character_count": 72,
  "wcag_compliant": true,
  "keyword_included": true
}
```

---

## Verification Harness
- **Validator Engine**: JSON Schema + String Length Validator
- **Verification Rule**:
  1. `alt_text` length must be $\le 125$ characters.
  2. `alt_text` must NOT contain case-insensitive prefixes `"image of"`, `"picture of"`, or `"photo of"`.
  3. `character_count` must equal exact string length of `alt_text`.
- **Pass Criteria**: Concise, descriptive alt text under 125 chars with target keyword integration.
- **Escalation Action**: Truncate at last word boundary before 125 characters if generated string exceeds limit.
