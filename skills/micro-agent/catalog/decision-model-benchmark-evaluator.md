# Micro-Agent: `decision-model-benchmark-evaluator`

- **Domain**: Decision Models & Benchmark Evaluation (`decision-index` / `nanojev-rs`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~290 tokens (System: 100, Input: 60, Output: 130)

---

## System Prompt
```text
You are an automated decision-model benchmark evaluator.
Given a pairwise choice benchmark problem, ground-truth criterion, and model log-likelihood outputs for options A and B, determine the winner, compute Bradley-Terry probability, and check transitivity constraints.
Output ONLY valid JSON.
Do NOT output conversational text.
```

---

## Input Schema
```text
TASK: "Select higher clinical acuity: [A] Stage 2 Hypertension with headache vs [B] Isolated minor finger laceration"
MODEL_SCORE_A: 2.84
MODEL_SCORE_B: -1.15
GROUND_TRUTH: "A"
```

---

## Output Contract
```json
{
  "selected_option": "A",
  "is_correct": true,
  "score_delta": 3.99,
  "bradley_terry_prob": 0.9818,
  "margin_of_victory": "decisive",
  "transitivity_violation": false,
  "confidence_calibrated": true
}
```

---

## Verification Harness
- **Validator Engine**: JSON Schema + Float Calculation Validator
- **Verification Rule**:
  1. `score_delta` must equal `MODEL_SCORE_A - MODEL_SCORE_B`.
  2. `bradley_terry_prob` must equal `1.0 / (1.0 + exp(-score_delta))`.
  3. `is_correct` must be boolean matching ground truth.
- **Pass Criteria**: Mathematical exactness of probability calculation and win classification.
- **Escalation Action**: Flag uncertain cases (`bradley_terry_prob` between 0.45 and 0.55) for human adjudication.
