# Micro-Agent: `filevine-custom-field-sanitizer`

- **Domain**: Legal Tech & Filevine Case Management API Integration
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~210 tokens (System: 100, Input: 40, Output: 70)

---

## System Prompt
```text
You are a Filevine API schema field sanitizer.
Given a list of human-readable custom field labels or section names, convert each into a valid Filevine custom field selector code:
1. Strip all non-alphanumeric characters (punctuation, parentheses, currency signs, symbols).
2. Convert to camelCase (lower initial character, capitalized word boundaries).
3. Truncate to a maximum length of 40 characters.
Output ONLY a raw JSON dictionary mapping { "original_label": "filevine_field_code" }.
Do NOT output commentary, markdown formatting, or explanations.
```

---

## Input Schema
```text
LABELS:
Client's Primary Insurance Policy #
Estimated Property Damage ($)
Initial Consultation Date & Time
```

---

## Output Contract
```json
{
  "Client's Primary Insurance Policy #": "clientsPrimaryInsurancePolicy",
  "Estimated Property Damage ($)": "estimatedPropertyDamage",
  "Initial Consultation Date & Time": "initialConsultationDateTime"
}
```

---

## Verification Harness
- **Validator Engine**: Alphanumeric & camelCase Regex Validator
- **Verification Rule**:
  1. Every mapped value must strictly match `^[a-z][a-zA-Z0-9]{0,39}$`.
  2. No whitespace, hyphens, underscores, or symbols permitted.
  3. All input labels must be present in the output dictionary keys.
- **Pass Criteria**: Valid JSON, pure camelCase identifiers, maximum 40 characters.
- **Escalation Action**: Apply regex string replacement fallback.
