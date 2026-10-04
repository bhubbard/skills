# Micro-Agent: `e164-phone-normalizer`

- **Domain**: Telephony, CRM & Dynamic Number Insertion (`fonoster`, `callrail-clone`, `ringcentral-rs`)
- **Target Runtime**: `apfel-rs` / Tier 0 Deterministic
- **Total Budget**: ~230 tokens (System: 90, Input: 35, Output: 105)

---

## System Prompt
```text
You are a telecommunications E.164 phone number canonicalizer.
Parse the raw telephone number and country context.
Strip formatting characters, prepend correct international country dialing code, and validate length.
Output ONLY a strictly valid JSON object.
Do NOT include commentary.
```

---

## Input Schema
```text
RAW_NUMBER: "(800) 522-6222 ext 104"
DEFAULT_COUNTRY: "US"
```

---

## Output Contract
```json
{
  "e164": "+18005226222",
  "country_code": "1",
  "national_number": "8005226222",
  "extension": "104",
  "is_valid": true,
  "formatted_national": "(800) 522-6222",
  "is_toll_free": true
}
```

---

## Verification Harness
- **Validator Engine**: E.164 Regex & Length Validator / Tier 0 Python Engine
- **Verification Rule**:
  1. `e164` must match regex `^\+[1-9]\d{1,14}$`.
  2. For US numbers, national number length must be exactly 10 digits.
  3. Toll-free prefix detection (800, 888, 877, 866, 855, 844, 833).
- **Pass Criteria**: Standardized E.164 output conforming to ITU-T recommendation.
- **Escalation Action**: Set `is_valid: false` when input has insufficient digits (<7 digits).
