# Micro-Agent: `schema-validator`

- **Domain**: Data Formatting & Schema Healing
- **Target Runtime**: `apfel-rs` / `zev-rs`
- **Total Budget**: ~400 tokens (System: 110, Input: 200, Output: 90)

---

## System Prompt
```text
You are a deterministic JSON schema healer.
Given potentially truncated, malformed, or unescaped JSON, output ONLY valid, syntactically clean, formatted JSON.
Do not output markdown code fences, comments, or explanations.
```

---

## Input Schema
```text
{
  "name": "wan-video",
  "status": "active",
  "tags": ["video", "generative"
```

---

## Output Contract
```json
{
  "name": "wan-video",
  "status": "active",
  "tags": ["video", "generative"]
}
```

---

## Verification Harness
- **Validator Engine**: `serde_json::from_str::<serde_json::Value>`
- **Verification Rule**:
  1. Parse output string with `serde_json`.
  2. Verify zero trailing characters, syntax errors, or unescaped tokens.
- **Pass Criteria**: Successful JSON deserialization with exit code 0.
- **Escalation Action**: Escalate to Tier 2 if output fails JSON parsing.
