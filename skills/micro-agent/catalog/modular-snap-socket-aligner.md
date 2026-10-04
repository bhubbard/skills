# Micro-Agent: `modular-snap-socket-aligner`

- **Domain**: 3D Modular Kitbashing & Snapping (`modly-rs` / `box3d-rs`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~280 tokens (System: 100, Input: 60, Output: 120)

---

## System Prompt
```text
You are a 3D modular asset snap socket aligner.
Given source socket A (pos, normal, up) and target socket B (pos, normal, up), calculate the rigid affine transformation (translation vector and rotation quaternion [x, y, z, w]) to snap socket A into socket B such that their normals oppose each other (normal_A = -normal_B) and up vectors align.
Output ONLY valid JSON.
```

---

## Input Schema
```text
SOCKET_A: { "pos": [2.0, 0.0, 0.0], "normal": [1.0, 0.0, 0.0], "up": [0.0, 1.0, 0.0], "type": "wall_joint" }
SOCKET_B: { "pos": [10.0, 0.0, 5.0], "normal": [0.0, 0.0, -1.0], "up": [0.0, 1.0, 0.0], "type": "wall_joint" }
```

---

## Output Contract
```json
{
  "translation": [10.0, 0.0, 3.0],
  "rotation_quat": [0.0, 0.7071, 0.0, 0.7071],
  "is_compatible": true,
  "socket_type": "wall_joint",
  "alignment_error": 0.0
}
```

---

## Verification Harness
- **Validator Engine**: Quaternion & Matrix Linear Algebra Validator (`glam` / `scipy`)
- **Verification Rule**:
  1. `rotation_quat` must be normalized unit quaternion ($\sum q_i^2 = 1.0 \pm 1e-4$).
  2. Rotating `normal_A` by `rotation_quat` must equal `-normal_B`.
  3. `translation` vector added to rotated `pos_A` must equal `pos_B`.
- **Pass Criteria**: Exact 3D rigid transform mapping socket A flush to socket B.
- **Escalation Action**: If socket types mismatch (e.g. `wall_joint` vs `door_frame`), set `is_compatible: false`.
