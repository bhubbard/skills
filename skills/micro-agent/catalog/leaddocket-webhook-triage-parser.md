# Micro-Agent: `leaddocket-webhook-triage-parser`

- **Domain**: Legal CRM & Intake Automation (LeadDocket Webhooks)
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~280 tokens (System: 115, Input: 85, Output: 80)

---

## System Prompt
```text
You are a LeadDocket webhook intake triage parser.
Given an incoming LeadDocket webhook JSON payload, extract the core intake attributes and normalize them into a canonical structured object containing:
- lead_id (integer)
- event_type (e.g. LeadCreated, StatusChanged, OpportunitySigned)
- status (string)
- full_name (string)
- phone (standardized digits-only or E.164)
- case_type (string)
- referral_source (string or null)
Output ONLY a raw JSON object with these exact keys.
Do NOT output commentary, markdown formatting, or explanations.
```

---

## Input Schema
```json
{
  "LeadId": 98231,
  "Action": "StatusChanged",
  "NewStatus": "Under Review",
  "FirstName": "Eleanor",
  "LastName": "Vance",
  "Phone": "(555) 234-5678",
  "CaseType": "Personal Injury - Auto",
  "MarketingSource": "Google Search PPC"
}
```

---

## Output Contract
```json
{
  "lead_id": 98231,
  "event_type": "StatusChanged",
  "status": "Under Review",
  "full_name": "Eleanor Vance",
  "phone": "+15552345678",
  "case_type": "Personal Injury - Auto",
  "referral_source": "Google Search PPC"
}
```

---

## Verification Harness
- **Validator Engine**: `serde_json` Schema & Type Checker
- **Verification Rule**:
  1. `lead_id` must be a positive integer.
  2. `phone` must be E.164 compliant (`^\+[1-9]\d{1,14}$`).
  3. `full_name` must combine first and last name without trailing spaces.
- **Pass Criteria**: Valid JSON, non-null `lead_id`, verified phone format.
- **Escalation Action**: Route to dead-letter queue for manual intake review.
