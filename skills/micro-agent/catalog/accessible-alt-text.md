# Micro-Agent: `accessible-alt-text`

- **Domain**: Web Accessibility (WCAG 2.2 AA) & SEO (`apfel-alt-text`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~320 tokens (System: 100, Input: 140, Output: 80)

---

## System Prompt
```text
You are a WCAG accessibility compliance expert.
Given surrounding HTML context, image filename, and page topic, generate concise, descriptive `alt` text under 125 characters.
Rules:
1. Do NOT start with "Photo of" or "Image of".
2. Describe the functional visual intent and emotional context.
3. If purely decorative, return `""` (empty string).
Output ONLY the alt text attribute value.
```

---

## Input Schema
```text
PAGE TOPIC: Emergency Personal Injury Lawyer Consultations
FILENAME: doctor-showing-mri-scan-to-patient.webp
SURROUNDING HTML:
<div class="case-review">
  <img src="doctor-showing-mri-scan-to-patient.webp" />
  <h3>Documenting Your Medical Trajectory</h3>
</div>
```

---

## Output Contract
```text
Doctor in white coat reviewing spine MRI scans with seated patient during consultation
```

---

## Verification Harness
- **Validator Engine**: Invariant String Linter
- **Verification Rule**: 
  1. String length must be between 10 and 150 characters: `10 <= len(output.strip()) <= 150`.
  2. Output must NOT start with boilerplate prefixes (`image of`, `picture of`, `photo of`, `graphic of`).
  3. Output must contain at least 3 distinct descriptive words.
- **Pass Criteria**: Meets all 3 length and quality criteria.
- **Escalation Action**: If criteria fail, re-prompt with explicit character length limits or escalate to Tier 2.
