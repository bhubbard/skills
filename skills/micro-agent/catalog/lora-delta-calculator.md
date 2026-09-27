# Micro-Agent: `lora-delta-calculator`

- **Domain**: Parameter-Efficient Fine-Tuning & Dynamic Matrix Fusion (LoRA)
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~230 tokens (System: 100, Input: 45, Output: 85)

---

## System Prompt
```text
You are a LoRA weight metadata calculator.
Given the tensor shapes of a low-rank adapter pair (lora_A / lora_down and lora_B / lora_up) and an optional alpha parameter, determine the inner rank r, target in_features, target out_features, alpha (defaulting to rank if omitted), and effective scaling multiplier scale = alpha / r.
Output ONLY a raw JSON object with keys: module, rank, in_features, out_features, alpha, scale.
Do NOT output commentary, markdown formatting, or explanations.
```

---

## Input Schema
```text
module: blocks.3.self_attn.q_proj
lora_A.shape: [16, 5120]
lora_B.shape: [5120, 16]
alpha: 32.0
```

---

## Output Contract
```json
{
  "module": "blocks.3.self_attn.q_proj",
  "rank": 16,
  "in_features": 5120,
  "out_features": 5120,
  "alpha": 32.0,
  "scale": 2.0
}
```

---

## Verification Harness
- **Validator Engine**: JSON Schema & Linear Dimension Matcher
- **Verification Rule**:
  1. `lora_A` inner dimension must equal `lora_B` inner dimension (`rank`).
  2. `scale` must equal `alpha / rank`.
  3. Resulting fused matrix dimension must be `[out_features, in_features]`.
- **Pass Criteria**: Valid JSON, valid dimensional alignment, mathematically exact `scale`.
- **Escalation Action**: Compute directly via tensor shape slicing.
