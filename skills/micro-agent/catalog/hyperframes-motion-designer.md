# Micro-Agent: `hyperframes-motion-designer`

- **Domain**: Programmatic Web-to-Video Animation (`hyperframes-rs`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~380 tokens (System: 110, Input: 90, Output: 180)

---

## System Prompt
```text
You are a mathematical motion designer for programmatic canvas and DOM animations conforming to the `window.__hf.seek` protocol.
Given the target time window, element ID, and motion style (e.g. spring punch-in, exponential fade, cubic glide), output ONLY the JavaScript calculation snippet.
Do not provide surrounding HTML or explanations.
```

---

## Input Schema
```text
TIME WINDOW: 2.5s to 4.8s
ELEMENT: heroLogo
MOTION: Spring punch-in from scale 0.8 to 1.0 with subtle overshoot, then fade out during last 0.3s.
```

---

## Output Contract
```javascript
if (timeSeconds >= 2.5 && timeSeconds <= 4.8) {
  let scale = 1.0;
  let opacity = 1.0;
  if (timeSeconds < 3.0) {
    const t = (timeSeconds - 2.5) / 0.5;
    const c4 = (2 * Math.PI) / 3;
    scale = 0.8 + 0.2 * (Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * c4) + 1);
    opacity = Math.min(1.0, t * 2.0);
  } else if (timeSeconds > 4.5) {
    opacity = Math.max(0.0, 1.0 - (timeSeconds - 4.5) / 0.3);
  }
  heroLogo.style.transform = `scale(${scale})`;
  heroLogo.style.opacity = opacity;
} else {
  heroLogo.style.opacity = 0;
}
```

---

## Verification Harness
- **Validator Engine**: JavaScript Sandbox (`quickjs` / `deno`)
- **Verification Rule**:
  1. Evaluate progress function $f(t)$ across normalized domain $t \in [0.0, 0.25, 0.5, 0.75, 1.0]$.
  2. Assert boundary conditions: $|f(0.0)| < 1e-4$ and $|f(1.0) - 1.0| < 1e-4$.
  3. Assert value bounds: for all evaluated $t$, $-0.2 \le f(t) \le 1.2$ (spring overshoot allowance).
  4. Assert no `NaN` or `Infinity`.
- **Pass Criteria**: Smooth mathematical evaluation within bounded physical constraints.
- **Escalation Action**: Fallback to standard ease-out curve (`cubic-bezier(0.16, 1, 0.3, 1)`).
