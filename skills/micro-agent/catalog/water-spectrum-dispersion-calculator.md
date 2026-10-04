# Micro-Agent: `water-spectrum-dispersion-calculator`

- **Domain**: Fluid Physics & Ocean Waves (`clearwater-rs`)
- **Target Runtime**: `apfel-rs` / Tier 0 Deterministic
- **Total Budget**: ~240 tokens (System: 95, Input: 45, Output: 100)

---

## System Prompt
```text
You are an ocean wave dispersion calculator.
Given wavenumber k, water depth d, gravity g, and surface tension sigma, compute the finite-depth dispersion frequency omega = sqrt((g*k + sigma*k^3) * tanh(k*d)), wavelength, phase speed, and 60-second quantized loop frequency.
Output ONLY valid JSON.
```

---

## Input Schema
```text
WAVENUMBER_K: 2.5
DEPTH: 1.6
GRAVITY: 9.81
SURFACE_TENSION: 0.000074
LOOP_PERIOD: 60.0
```

---

## Output Contract
```json
{
  "wavenumber": 2.5,
  "depth": 1.6,
  "wavelength_m": 2.5133,
  "angular_frequency_rad_s": 4.9515,
  "phase_speed_m_s": 1.9806,
  "quantized_omega": 4.9218,
  "regime": "transitional_depth"
}
```

---

## Verification Harness
- **Validator Engine**: Deterministic Physics Equation / Tier 0 Engine
- **Verification Rule**:
  1. `wavelength_m` must equal `2 * pi / k`.
  2. `phase_speed_m_s` must equal `angular_frequency_rad_s / k`.
  3. `quantized_omega` must be a multiple of `2 * pi / LOOP_PERIOD`.
- **Pass Criteria**: Mathematical exactness of Airy wave dispersion in finite water depth.
- **Escalation Action**: Deep water approximation $\omega = \sqrt{g k}$ when $k \cdot d > 3.0$.
