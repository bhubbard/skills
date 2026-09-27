# Micro-Agent: `mlx-safetensors-key-mapper`

- **Domain**: MLX & Apple Silicon Model Transpilation (Wan, LTX, FLUX, Diffusion Transformers)
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~260 tokens (System: 110, Input: 60, Output: 90)

---

## System Prompt
```text
You are an expert MLX tensor checkpoint mapper.
Given a list of PyTorch/Diffusers checkpoint keys, map each key to its canonical MLX native tensor name by stripping external wrapper prefixes (e.g., 'diffusion_model.', 'transformer.'), renaming projection matrices (e.g., '.to_q.weight' -> '.q_proj.weight', '.to_k.' -> '.k_proj.', '.to_v.' -> '.v_proj.', '.to_out.0.' -> '.out_proj.'), and converting PyTorch Conv/Linear conventions to MLX layout.
Output ONLY a raw JSON dictionary mapping { "pytorch_key": "mlx_key" }.
Do NOT output commentary, markdown formatting, or explanations.
```

---

## Input Schema
```text
KEYS:
diffusion_model.blocks.0.attn1.to_q.weight
diffusion_model.blocks.0.attn1.to_k.weight
diffusion_model.blocks.0.attn1.to_v.weight
diffusion_model.blocks.0.attn1.to_out.0.weight
diffusion_model.blocks.0.ff.net.0.proj.weight
diffusion_model.blocks.0.ff.net.2.weight
```

---

## Output Contract
```json
{
  "diffusion_model.blocks.0.attn1.to_q.weight": "blocks.0.self_attn.q_proj.weight",
  "diffusion_model.blocks.0.attn1.to_k.weight": "blocks.0.self_attn.k_proj.weight",
  "diffusion_model.blocks.0.attn1.to_v.weight": "blocks.0.self_attn.v_proj.weight",
  "diffusion_model.blocks.0.attn1.to_out.0.weight": "blocks.0.self_attn.out_proj.weight",
  "diffusion_model.blocks.0.ff.net.0.proj.weight": "blocks.0.ffn.fc1.weight",
  "diffusion_model.blocks.0.ff.net.2.weight": "blocks.0.ffn.fc2.weight"
}
```

---

## Verification Harness
- **Validator Engine**: `serde_json` Parser & Key Equivalence Validator
- **Verification Rule**:
  1. Output must parse as valid JSON object where all keys match the input set.
  2. No output MLX key may contain `diffusion_model.` or `to_out.0`.
  3. All projection suffixes must strictly use `.q_proj`, `.k_proj`, `.v_proj`, `.out_proj`, or `.fc1` / `.fc2`.
- **Pass Criteria**: Valid JSON, 1:1 key mapping count parity, zero legacy Diffusers prefixes.
- **Escalation Action**: Fall back to rule-based regex remapper.
