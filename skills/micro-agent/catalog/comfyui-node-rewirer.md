# Micro-Agent: `comfyui-node-rewirer`

- **Domain**: ComfyUI Node Graph Routing & Type Safety (`comfyui-ltxvideo-mlx-rs`)
- **Target Runtime**: `apfel-rs` / `zev-rs`
- **Total Budget**: ~420 tokens (System: 120, Input: 180, Output: 120)

---

## System Prompt
```text
You are a ComfyUI node graph rewirer.
Given source node output specifications and destination node input slots, determine socket type compatibility (e.g. MODEL, VAE, CONDITIONING, LATENT, IMAGE, AUDIO).
Output ONLY the valid JSON link array connecting the compatible sockets, or an error reason if incompatible.
```

---

## Input Schema
```text
SOURCE NODE:
id: 3, class_type: "LTXVMLXTwoStageHQSampler", outputs: ["LATENT", "AUDIO"]

DESTINATION NODE:
id: 6, class_type: "LTXVMLXVAEDecode", inputs: {"samples": "LATENT", "vae": "VAE"}
```

---

## Output Contract
```json
{
  "link": {
    "source_node_id": 3,
    "source_output_slot": 0,
    "target_node_id": 6,
    "target_input_slot": "samples",
    "socket_type": "LATENT"
  }
}
```

---

## Verification Harness
- **Validator Engine**: ComfyUI Directed Graph Validator
- **Verification Rule**:
  1. Parse modified graph JSON via `serde_json`.
  2. Validate node existence: source and destination node IDs must exist in the graph.
  3. Validate socket type parity: output socket type must strictly match destination input socket type (e.g. `MODEL` to `MODEL`, `IMAGE` to `IMAGE`).
- **Pass Criteria**: Valid DAG topology with matching socket data types.
- **Escalation Action**: Reject invalid connection and escalate to Tier 2.
