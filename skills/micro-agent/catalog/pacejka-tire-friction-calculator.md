# Micro-Agent: `pacejka-tire-friction-calculator`

- **Domain**: Vehicle Dynamics & Physics Simulation (`tlab-vehicle-physics-rs` / `simplecar2-rs`)
- **Target Runtime**: `apfel-rs` / Tier 0 Deterministic
- **Total Budget**: ~260 tokens (System: 100, Input: 50, Output: 110)

---

## System Prompt
```text
You are a vehicle tire dynamics calculator.
Given slip angle alpha (degrees), normal load Fz (Newtons), and Pacejka Magic Formula coefficients (B, C, D, E), evaluate lateral cornering force Fy = D * sin(C * arctan(B * alpha - E * (B * alpha - arctan(B * alpha)))).
Output ONLY valid JSON.
Do NOT include commentary.
```

---

## Input Schema
```text
SLIP_ANGLE_DEG: 4.5
NORMAL_LOAD_FZ: 4000.0
PACEJKA_B: 10.0
PACEJKA_C: 1.30
PACEJKA_D: 1.00
PACEJKA_E: -0.90
```

---

## Output Contract
```json
{
  "slip_angle_deg": 4.5,
  "normal_load_fz_n": 4000.0,
  "lateral_force_fy_n": 3728.6,
  "peak_friction_coeff": 1.0,
  "grip_saturation_pct": 93.2,
  "regime": "linear_to_peak"
}
```

---

## Verification Harness
- **Validator Engine**: Deterministic Magic Formula Equation / Tier 0 Engine
- **Verification Rule**:
  1. Lateral force must not exceed peak friction $D \times F_z$.
  2. For zero slip angle, force must equal 0.0.
  3. Sign of lateral force must match sign of slip angle.
- **Pass Criteria**: Mathematical exactness of Pacejka 1993 tire characteristic curve.
- **Escalation Action**: Linear brush model approximation if slip angle is under 0.5 degrees.
