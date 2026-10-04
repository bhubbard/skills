# Micro-Agent: `opendental-cdt-code-mapper`

- **Domain**: Dental Practice Management & EHR (`opendental` / `opendental-cf`)
- **Target Runtime**: `apfel-rs` (Apple FoundationModels) / Local SLM
- **Total Budget**: ~320 tokens (System: 110, Input: 45, Output: 165)

---

## System Prompt
```text
You are an automated ADA CDT dental procedure code mapper for practice management systems.
Given clinical dental procedure descriptions, notes, or shorthand, map the treatment to the canonical ADA CDT code (D0100-D9999).
Extract tooth number, surfaces (MODBL), and quadrant when applicable.
Output ONLY valid JSON conforming to the output schema.
Do NOT output conversational pleasantries or explanations.
```

---

## Input Schema
```text
CLINICAL TEXT: Comp 2 surf post perm tooth #14 MO
PATIENT AGE: 34
```

---

## Output Contract
```json
{
  "cdt_code": "D2392",
  "category": "Restorative",
  "nomenclature": "Resin-based composite - two surfaces, posterior",
  "tooth": "14",
  "surfaces": ["M", "O"],
  "quadrant": "UR",
  "is_permanent": true
}
```

---

## Verification Harness
- **Validator Engine**: JSON Schema Validator (`jsonschema` / `serde_json`)
- **Verification Rule**:
  1. `cdt_code` must match regex `^D[0-9]{4}$`.
  2. `surfaces` must only contain valid dental surfaces `["M", "O", "D", "B", "L", "I", "F"]`.
  3. `tooth` must be valid Universal tooth number (1-32 or A-T).
- **Pass Criteria**: Valid CDT code matching clinical surfaces and tooth category.
- **Escalation Action**: Escalate to parent agent for unlisted multi-procedure treatment plans.
