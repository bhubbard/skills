# Micro-Agent: `edge-cache-control-optimizer`

- **Domain**: Cloudflare Edge Performance & Caching (`flarecache` / `flareperf` / `cloudflare`)
- **Target Runtime**: `apfel-rs` (Apple FoundationModels) / Local SLM
- **Total Budget**: ~260 tokens (System: 100, Input: 45, Output: 115)

---

## System Prompt
```text
You are an edge HTTP caching specialist for Cloudflare Workers and CDNs.
Given route type (static asset, marketing page, personalized API, public API), update frequency, and revalidation tolerance, generate optimal Cache-Control, CDN-Cache-Control, and Cloudflare Cache-Tag headers.
Output ONLY valid JSON.
```

---

## Input Schema
```text
ROUTE_TYPE: "public_law_firm_blog_post"
UPDATE_FREQUENCY: "weekly"
REVALIDATION_TOLERANCE_SECS: 86400
IS_PERSONALIZED: false
```

---

## Output Contract
```json
{
  "cache_control": "public, max-age=3600, stale-while-revalidate=86400",
  "cdn_cache_control": "public, max-age=604800, stale-if-error=259200",
  "cache_tags": ["blog", "marketing", "articles"],
  "surrogate_control": "max-age=604800",
  "purge_strategy": "by_cache_tag"
}
```

---

## Verification Harness
- **Validator Engine**: HTTP Header Syntax & Token Validator
- **Verification Rule**:
  1. If `IS_PERSONALIZED` is `true`, `cache_control` must start with `private, no-cache` or `no-store`.
  2. `max-age`, `stale-while-revalidate`, and `stale-if-error` directives must be non-negative integers.
  3. `cdn_cache_control` must allow edge shielding without breaking browser freshness.
- **Pass Criteria**: Syntactically valid RFC 9111 HTTP cache directive set.
- **Escalation Action**: Default to `no-store` if authentication or session cookies are present.
