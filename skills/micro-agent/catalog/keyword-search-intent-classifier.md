# Micro-Agent: `keyword-search-intent-classifier`

- **Domain**: SEO Search Strategy & Intent Mapping (`serpbear` / `frontlane-serp`)
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~240 tokens (System: 90, Input: 40, Output: 110)

---

## System Prompt
```text
You are an SEO keyword intent classifier.
Classify the given search query into primary intent: Informational, Navigational, Commercial Investigation, or Transactional.
Identify secondary intent, sales funnel stage (Top/Middle/Bottom), and the recommended content page template.
Output ONLY valid JSON.
```

---

## Input Schema
```text
QUERY: "best car accident attorney fees in orange county"
```

---

## Output Contract
```json
{
  "query": "best car accident attorney fees in orange county",
  "primary_intent": "Commercial Investigation",
  "secondary_intent": "Transactional",
  "funnel_stage": "Bottom",
  "recommended_template": "comparison_landing_page",
  "has_local_intent": true
}
```

---

## Verification Harness
- **Validator Engine**: JSON Schema Validator
- **Verification Rule**:
  1. `primary_intent` must be one of `["Informational", "Navigational", "Commercial Investigation", "Transactional"]`.
  2. `funnel_stage` must be one of `["Top", "Middle", "Bottom"]`.
  3. `has_local_intent` must be boolean.
- **Pass Criteria**: Standard intent taxonomy matching query modifier cues (e.g. "best", "fees", geographic location).
- **Escalation Action**: Default to "Informational" if query is ambiguous or single-word.
