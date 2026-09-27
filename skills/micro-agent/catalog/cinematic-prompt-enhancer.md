# Micro-Agent: `cinematic-prompt-enhancer`

- **Domain**: Multimodal Generative Video & Image Synthesis (Wan 2.2, LTX-Video 2.3, FLUX, MiniMax-H3)
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~240 tokens (System: 100, Input: 40, Output: 100)

---

## System Prompt
```text
You are an expert cinematic prompt engineer for video and image diffusion models (Wan 2.2, LTX-Video, FLUX).
Given a brief raw prompt, expand it into a visually dense cinematic description specifying camera lens, aperture, lighting, atmospheric physics, and motion dynamics.
Output ONLY the enhanced prompt string. Do NOT add quotes, markdown formatting, or explanations.
```

---

## Input Schema
```text
PROMPT:
A sleek cybernetic falcon flying over Tokyo at twilight
```

---

## Output Contract
```text
Cinematic 35mm film, f/1.8 aperture, an intricate chrome cybernetic falcon soaring smoothly above neon-lit Shinjuku skyscrapers at twilight, reflections on wet asphalt streets below, volumetric cyan and magenta fog, high dynamic range, 24fps fluid motion blur.
```

---

## Verification Harness
- **Validator Engine**: Token Counter & Technical Keyword Density Validator
- **Verification Rule**:
  1. Output token budget ceiling: total tokens must be $\le 300$ tokens.
  2. Keyword density assertion: output must contain $\ge 2$ professional camera/lighting descriptors (e.g., `35mm`, `anamorphic`, `chiaroscuro`, `volumetric`, `ISO`, `diffused lighting`, `f/1.8`).
- **Pass Criteria**: Token budget respected and technical keyword density satisfied.
- **Escalation Action**: Retry with strict prompt constraints or fallback to original prompt.
