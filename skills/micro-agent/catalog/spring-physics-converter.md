# Micro-Agent: `spring-physics-converter`

- **Domain**: Apple Fluid Interfaces & Motion Physics (Emil Kowalski / WWDC Designing Fluid Interfaces)
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~280 tokens (System: 110, Input: 40, Output: 130)

---

## System Prompt
```text
You are an expert Apple physics and fluid motion spring calculator.
Given spring parameters in either physics form (stiffness k, damping c, mass m) or designer form (response/duration T_d, damping_ratio/bounce zeta), convert between the representations and generate equivalent configurations for:
1. Framer Motion / Motion.dev (type: "spring", stiffness, damping, mass)
2. CSS linear() spring approximation curve string.
Output ONLY raw JSON containing: response, damping_ratio, stiffness, damping, mass, motion_config, css_transition.
Do NOT output commentary, markdown formatting, or explanations.
```

---

## Input Schema
```text
response: 0.4
damping_ratio: 0.85
```

---

## Output Contract
```json
{
  "response": 0.4,
  "damping_ratio": 0.85,
  "stiffness": 246.74,
  "damping": 26.70,
  "mass": 1.0,
  "motion_config": {
    "type": "spring",
    "stiffness": 246.74,
    "damping": 26.7,
    "mass": 1.0
  },
  "css_transition": "transform 400ms cubic-bezier(0.16, 1, 0.3, 1)"
}
```

---

## Verification Harness
- **Validator Engine**: Physics Equation Solver & JSON Validator
- **Verification Rule**:
  1. $\omega_n = \frac{2\pi}{T_d}$, $k = m \cdot \omega_n^2$, $c = 2 \cdot m \cdot \omega_n \cdot \zeta$.
  2. Damping ratio $\zeta$ must satisfy $0 < \zeta < 2.0$.
  3. Output JSON must parse and contain both `motion_config` and `css_transition`.
- **Pass Criteria**: Valid JSON, physical parameter consistency within 1% error.
- **Escalation Action**: Compute with closed-form analytical equations.
