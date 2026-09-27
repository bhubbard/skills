# Micro-Agent: `astro-schema-ld-scaffolder`

- **Domain**: Technical SEO & Schema.org Structured Data Graphs (`bhubbard.github.io`, `astro-schema-ld-verifier`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~520 tokens (System: 120, Input: 120, Output: 280)

---

## System Prompt
```text
You are an expert technical SEO schema architect.
Given an Astro markdown frontmatter block, generate valid, indented Schema.org JSON-LD graph metadata conforming to Article, WebSite, or TechArticle specifications.
Output ONLY the `<script type="application/ld+json">` HTML block.
```

---

## Input Schema
```yaml
title: "Zero-Token LLM Decision Engines in Rust"
description: "How Zev achieves 5.8 microsecond order-invariant inference without model weights."
pubDate: 2026-09-24
author: "Brandon Hubbard"
url: "https://code.brandonhubbard.com/zev-rs/"
```

---

## Output Contract
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "Zero-Token LLM Decision Engines in Rust",
  "description": "How Zev achieves 5.8 microsecond order-invariant inference without model weights.",
  "datePublished": "2026-09-24",
  "author": {
    "@type": "Person",
    "name": "Brandon Hubbard",
    "url": "https://brandonhubbard.com"
  },
  "mainEntityOfPage": "https://code.brandonhubbard.com/zev-rs/"
}
</script>
```

---

## Verification Harness
- **Validator Engine**: `serde_json` + Schema.org Structure Validator
- **Verification Rule**:
  1. Extract `<script type="application/ld+json">` contents and parse via `serde_json::from_str`.
  2. Verify top-level `@context` strictly equals `"https://schema.org"` (or `"http://schema.org"`).
  3. Verify `@type` is a recognized Schema.org entity (e.g. `Article`, `BlogPosting`, `Person`, `Organization`, `WebSite`).
- **Pass Criteria**: Syntactically valid JSON-LD graph with valid `@context` and non-empty `@type`.
- **Escalation Action**: On malformed JSON or invalid schema entity, escalate to Tier 2.
