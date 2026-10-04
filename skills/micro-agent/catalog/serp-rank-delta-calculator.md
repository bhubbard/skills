# Micro-Agent: `serp-rank-delta-calculator`

- **Domain**: Search Engine Position Tracking (`serpbear` / `serpbear-rs` / `frontlane-serp`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~280 tokens (System: 100, Input: 60, Output: 120)

---

## System Prompt
```text
You are an automated SEO rank volatility and displacement calculator.
Given current position, previous position, and detected SERP features, compute displacement metrics, movement status, and visibility changes.
Output ONLY a strictly valid JSON object.
Do NOT include explanations.
```

---

## Input Schema
```text
KEYWORD: "personal injury lawyer los angeles"
CURRENT_POSITION: 4
PREVIOUS_POSITION: 7
SERP_FEATURES_DETECTED: ["local_pack", "people_also_ask", "site_links"]
```

---

## Output Contract
```json
{
  "current_rank": 4,
  "previous_rank": 7,
  "delta": 3,
  "direction": "up",
  "status": "improved",
  "page_one": true,
  "top_three": false,
  "serp_features": ["local_pack", "people_also_ask", "site_links"],
  "volatility_score": 0.3
}
```

---

## Verification Harness
- **Validator Engine**: JSON Schema + Deterministic Delta Validator
- **Verification Rule**:
  1. `delta` must equal `previous_rank - current_rank` (positive represents upward ranking gain).
  2. If `current_rank <= 10`, `page_one` must be `true`.
  3. If `current_rank <= 3`, `top_three` must be `true`.
- **Pass Criteria**: Mathematical consistency between rank values, delta, and directional status.
- **Escalation Action**: Flag rank drop $>10$ positions for immediate algorithm update anomaly triage.
