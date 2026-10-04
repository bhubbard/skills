# Micro-Agent: `fonoster-call-flow-scaffolder`

- **Domain**: Programmable Telephony & Voice Applications (`fonoster` / `fonoster-rs`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~340 tokens (System: 110, Input: 60, Output: 170)

---

## System Prompt
```text
You are a Fonoster Voice Application code scaffolder.
Given an IVR phone triage prompt, menu choices, and transfer destination, generate a zero-dependency Fonoster Voice JavaScript handler function using `@fonoster/voice`.
Include greeting, DTMF gather, choice branch, and fallback.
Output ONLY executable JavaScript code.
Do NOT include markdown explanations or conversational text.
```

---

## Input Schema
```text
GREETING: "Thank you for calling Call Jacob Law Firm."
MENU: "Press 1 for New Accidents. Press 2 for Existing Clients."
TRANSFER_1: "+18005226222"
TRANSFER_2: "+18005226223"
FALLBACK: "We did not receive your selection. Please hold."
```

---

## Output Contract
```text
async function voiceHandler(req, res) {
  await res.answer();
  await res.say("Thank you for calling Call Jacob Law Firm.");
  const result = await res.gather({
    source: "speech_and_dtmf",
    numDigits: 1,
    timeout: 4,
    play: "Press 1 for New Accidents. Press 2 for Existing Clients."
  });

  if (result.digits === "1") {
    await res.dial("+18005226222");
  } else if (result.digits === "2") {
    await res.dial("+18005226223");
  } else {
    await res.say("We did not receive your selection. Please hold.");
    await res.dial("+18005226222");
  }
}
```

---

## Verification Harness
- **Validator Engine**: JavaScript Syntax Parser (`esprima` / `oxc`)
- **Verification Rule**:
  1. Verifies valid async function signature `async function voiceHandler(req, res)`.
  2. Ensures all telephony verbs (`res.answer`, `res.say`, `res.gather`, `res.dial`) are called with `await`.
  3. Ensures all phone destinations are formatted in E.164 notation.
- **Pass Criteria**: Clean AST parse with zero syntax errors.
- **Escalation Action**: Fallback to standard receptionist routing template on syntax failure.
