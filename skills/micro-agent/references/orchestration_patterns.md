# Micro-Agent Orchestration Patterns: Eliminating the Multi-Hop Tax

> **The Problem**: Chaining 6 micro-agents serially creates 6 network roundtrips, context degradation across serialization boundaries, and cumulative latency. Micro-agents must NEVER replace global systemic reasoning.

---

## 🏛️ The Three Valid Orchestration Modes

```
                    ┌──────────────────────────────────────────────┐
                    │      Frontier Agent (Claude / Gemini)        │
                    │   (Full 200k Context, System Architecture)   │
                    └──────────────────────┬───────────────────────┘
                                           │
                        Dispatches as Tools│ (Single Roundtrip)
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             The Fast Worker Toolbelt                             │
├───────────────────────────────┬──────────────────────────────────────────────────┤
│ Tier 0: Deterministic Engine  │ Tier 1: Constrained SLMs                         │
│ • flow_matching_sigmas()      │ • mlx-safetensors-key-mapper (Logit masked)     │
│ • filevine_sanitize()         │ • accessible-alt-text                            │
│ • spring_physics_convert()    │ • conventional-committer                         │
└───────────────────────────────┴──────────────────────────────────────────────────┘
```

---

### Mode 1: The Frontier Agent's Local Toolbelt (Recommended)
Instead of delegating the whole engineering job to a chain of micro-agents:
1. The **Frontier Model** maintains the full workspace context, architecture plan, and multi-file diffs.
2. The Frontier Model calls micro-agents and Tier 0 tools as **instantaneous tools** within its tool loop.
3. **Benefits**:
   - Zero context loss (the frontier model retains all lifetime, trait, and dependency knowledge).
   - Zero hallucination on math/regex (handled by Tier 0).
   - Token conservation on repetitive subtasks.

---

### Mode 2: Atomic Developer CLI Shortcuts
Standalone execution triggered directly from developer terminals or git hooks:
- `brandon commit`: Uses `conventional-committer` directly on `git diff --staged`.
- `brandon lint-fix`: Pipes compiler error stderr to `rustc-borrow-healer`.
- `brandon alt-text <image>`: Generates WCAG compliant description.

No frontier model required; runs 100% on-device via `apfel-rs` or local 1B–3B model.

---

### Mode 3: Composite Coarse Workflows
When a task inherently spans multiple concerns (e.g. creating a Cloudflare Worker with D1 database, Turnstile verification, and Wrangler bindings):
- **ANTI-PATTERN**: Chaining `cloudflare-d1-migration-maker` $\to$ `wrangler-binding-auditor` $\to$ `turnstile-edge-validator` in sequence.
- **BEST PRACTICE**: Combine into a single coarse-grained workflow where the prompt provides all three schemas simultaneously. The model generates the migration, binding TOML, and validation handler in **one single turn**.
