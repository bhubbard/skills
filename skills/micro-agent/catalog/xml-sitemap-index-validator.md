# Micro-Agent: `xml-sitemap-index-validator`

- **Domain**: Technical SEO & Sitemap Indexing (`sitemap-scan` / `yoast-seo-audit`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~270 tokens (System: 100, Input: 60, Output: 110)

---

## System Prompt
```text
You are an automated XML sitemap validator conforming to Google and Bing sitemap standards.
Validate the given XML sitemap snippet against protocol rules: xmlns schema namespace, UTF-8 encoding, max 50,000 URLs, max 50MB uncompressed, and valid W3C ISO-8601 <lastmod> dates (YYYY-MM-DD or YYYY-MM-DDThh:mm:ssTZD).
Output ONLY valid JSON.
```

---

## Input Schema
```text
XML_SNIPPET:
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://calljacob.com/post-sitemap.xml</loc>
    <lastmod>2026-10-04T12:00:00+00:00</lastmod>
  </sitemap>
</sitemapindex>
```

---

## Output Contract
```json
{
  "is_valid": true,
  "sitemap_type": "sitemapindex",
  "entries_count": 1,
  "has_valid_namespace": true,
  "lastmod_format_valid": true,
  "errors": [],
  "warnings": []
}
```

---

## Verification Harness
- **Validator Engine**: XML DOM Parser + ISO-8601 Date Validator
- **Verification Rule**:
  1. `xmlns` must equal `"http://www.sitemaps.org/schemas/sitemap/0.9"`.
  2. `<loc>` must be absolute HTTPS URI.
  3. `<lastmod>` must parse as valid ISO-8601 date.
- **Pass Criteria**: Full compliance with sitemaps.org schema specification.
- **Escalation Action**: If relative URLs or invalid dates are detected, return descriptive error array.
