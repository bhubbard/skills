# Micro-Agent: `obj-mesh-normal-recalculator`

- **Domain**: 3D Geometry & Generative Meshes (`hunyuan3d-rs` / `modly-rs`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~310 tokens (System: 100, Input: 80, Output: 130)

---

## System Prompt
```text
You are a 3D mesh normal calculator.
Given vertices [x, y, z] and triangle face indices [v0, v1, v2], calculate normalized unit face normals via cross product (v1 - v0) x (v2 - v0) and accumulate area-weighted vertex normals.
Output ONLY valid JSON containing the normalized vertex normals.
Do NOT include commentary.
```

---

## Input Schema
```text
VERTICES: [
  [0.0, 0.0, 0.0],
  [1.0, 0.0, 0.0],
  [0.0, 1.0, 0.0],
  [0.0, 0.0, 1.0]
]
FACES: [
  [0, 1, 2],
  [0, 3, 1],
  [0, 2, 3]
]
```

---

## Output Contract
```json
{
  "vertex_normals": [
    [-0.5774, -0.5774, -0.5774],
    [0.7071, 0.0, -0.7071],
    [0.0, 0.7071, -0.7071],
    [-0.7071, -0.7071, 0.0]
  ],
  "face_count": 3,
  "vertex_count": 4,
  "is_manifold": true
}
```

---

## Verification Harness
- **Validator Engine**: Vector Mathematics Validator (`glam` / `numpy`)
- **Verification Rule**:
  1. Each normal vector must have unit length $\approx 1.0 \pm 1e-3$.
  2. Number of normals must equal number of input vertices.
  3. No component may be `NaN` or `null`.
- **Pass Criteria**: Unit-length normalized vectors smoothly interpolating across shared face vertices.
- **Escalation Action**: If degenerate triangle area is 0, assign default vertical normal `[0.0, 1.0, 0.0]`.
