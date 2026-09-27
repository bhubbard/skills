---
name: micro-agent
description: |
  Design, build, and deploy 4,000-token strictly bounded micro-agents engineered to run reliably on on-device small language models (like apfel-rs on Apple Silicon, Apple FoundationModels, Chrome Built-in Gemini Nano, and 1B-3B local models). Use this skill whenever a user wants to create, design, optimize, or identify micro-agents, subagents with strict token budgets, on-device SLM task workers, or requests to decompose complex multi-step workflows into atomic, low-latency, zero-cost subagents. Also trigger continuously during engineering workflows to identify repetitive, bounded tasks that can be codified into reusable micro-agents.
---

# Micro-Agent Architecture & Design

Micro-agents are hyper-focused, single-responsibility subagents strictly constrained to a **4,000-token hard ceiling** across their entire lifecycle (System Prompt + Tool Schema + Input Context + Output Generation $\le$ 4,000 tokens).

Unlike generalist frontier agents designed for 128k–1M+ token windows, micro-agents are optimized for **on-device Small Language Models (SLMs)**:
- **`apfel-rs`** (Apple Intelligence FoundationModels on Apple Silicon NPU/Metal)
- **Chrome Built-in Gemini Nano**
- **Quantized Local 1B–3B Models** (Llama 3.2 1B/3B, Qwen 2.5 Coder 1.5B/3B, Gemma 2 2B)

When paired with zero-token mathematical decision engines like **[`zev-rs`](https://github.com/bhubbard/zev-rs)**, micro-agents create an edge cascade: microsecond zero-token classification $\to$ sub-100ms local micro-agent execution $\to$ zero network API cost.

---

## 📐 The 4,000-Token Budget Envelope

Every micro-agent must conform to the **4K Contract**:

| Component | Strict Token Budget | Optimization Technique |
| :--- | :--- | :--- |
| **System Prompt & Role** | **150 – 300 tokens** | Imperative, zero fluff, explicit output schema, no conversational persona. |
| **Tool Definition** | **0 – 300 tokens** | Zero-or-one tool policy. Prefer pure string-to-string transforms or JSON. |
| **Input Context Payload** | **2,000 – 2,500 tokens** | Pre-filtered AST slice, compiler stderr, or isolated function diff. Never entire files. |
| **Output Generation** | **500 – 1,000 tokens** | Direct replacement patch, structured JSON, or concise commit message. |
| **TOTAL** | **$\le$ 4,000 tokens** | **Guaranteed zero truncation on Apple Silicon FoundationModels.** |

---

## 🏛️ Micro-Agent Archetypes

Micro-agents strictly adhere to the **Single Responsibility Principle (SRP)**. Never combine multiple orthogonal tasks into one micro-agent.

```
                    ┌────────────────────────┐
                    │ Parent Agent / Zev-RS  │
                    └───────────┬────────────┘
              Cascades to       │ (< 4,000 tokens)
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
 ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
 │    Healer    │        │ Synthesizer  │        │  Classifier  │
 │(Compiler/Lint)│        │(Tests/Commits)│       │ (Route/Triage)│
 └──────────────┘        └──────────────┘        └──────────────┘
```

### 1. The Healer (Compiler & Lint Fixer)
- **Role**: Takes a compiler error diagnostic (`rustc`, `tsc`, `clippy`) and 15–30 surrounding code lines.
- **Output**: Unified patch or replacement lines.
- **Example**: [`catalog/rust-compiler-healer.md`](catalog/rust-compiler-healer.md), [`catalog/rustc-borrow-healer.md`](catalog/rustc-borrow-healer.md).

### 2. The Synthesizer (Tests & Documentation)
- **Role**: Takes an isolated struct/function signature and generates 3 edge-case tests or docstrings.
- **Output**: Code block with `#[test]` or standard doc comments.
- **Example**: [`catalog/unit-test-synthesizer.md`](catalog/unit-test-synthesizer.md).

### 3. The Committer (Changelog & Commits)
- **Role**: Takes `git diff --stat` and key diff chunks; produces conventional commit message.
- **Output**: `feat(scope): concise summary` + 3 bullet points.
- **Example**: [`catalog/conventional-committer.md`](catalog/conventional-committer.md).

### 4. The Transformer (AST & API Refactor)
- **Role**: Rewrites deprecated function calls or transforms one data structure into another.
- **Output**: Clean replacement code.
- **Example**: [`catalog/ast-refactor-transformer.md`](catalog/ast-refactor-transformer.md), [`catalog/glam-transform-bridge.md`](catalog/glam-transform-bridge.md).

### 5. The Schema Validator & Repairer
- **Role**: Takes malformed or incomplete JSON/YAML and repairs it to conform to a target schema.
- **Output**: Strictly valid JSON with zero conversational commentary.
- **Example**: [`catalog/schema-validator.md`](catalog/schema-validator.md), [`catalog/astro-schema-ld-scaffolder.md`](catalog/astro-schema-ld-scaffolder.md).

---

## 📚 Complete Micro-Agent Catalog (17 Agents)

| Micro-Agent | Primary Cluster | Role & Responsibility | Measured Tokens |
| :--- | :--- | :--- | :--- |
| [`cinematic-prompt-enhancer`](catalog/cinematic-prompt-enhancer.md) | Generative MLX | Expands raw prompts into 35mm cinematic lighting & camera specs | 258 tokens |
| [`hyperframes-motion-designer`](catalog/hyperframes-motion-designer.md) | HyperFrames | Generates mathematical Bezier & spring progress logic for `window.__hf` | 332 tokens |
| [`comfyui-node-rewirer`](catalog/comfyui-node-rewirer.md) | ComfyUI / LTX | Verifies socket type parity and links graph nodes | 227 tokens |
| [`bevy-component-scaffolder`](catalog/bevy-component-scaffolder.md) | Game Engine / ECS | Converts C++/GDScript gameplay structs into Bevy ECS components | 272 tokens |
| [`rustc-borrow-healer`](catalog/rustc-borrow-healer.md) | Rust Systems | Resolves E0382, E0499, and E0502 borrow-checker diagnostics | 256 tokens |
| [`rust-compiler-healer`](catalog/rust-compiler-healer.md) | Rust Systems | One-shot patch generator for syntax and type mismatch errors | 219 tokens |
| [`glam-transform-bridge`](catalog/glam-transform-bridge.md) | Game Physics | Synthesizes `glam::Mat4` and `glam::Quat` affine transformations | 252 tokens |
| [`tailwind-class-sorter`](catalog/tailwind-class-sorter.md) | Frontend CSS | Reorders utility classes by box-model cascade specificity | 240 tokens |
| [`accessible-alt-text`](catalog/accessible-alt-text.md) | A11y & SEO | Generates concise WCAG 2.2 AA compliant image descriptions | 244 tokens |
| [`natural-to-awk`](catalog/natural-to-awk.md) | CLI & Logs | Translates natural-language log extraction into single-line `awk` commands | 194 tokens |
| [`astro-schema-ld-scaffolder`](catalog/astro-schema-ld-scaffolder.md) | Astro Web | Generates valid Schema.org JSON-LD `<script>` graphs from frontmatter | 295 tokens |
| [`hydration-island-advisor`](catalog/hydration-island-advisor.md) | Astro Web | Recommends optimal island hydration directives (`client:visible`, etc.) | 282 tokens |
| [`cloudflare-d1-migration-maker`](catalog/cloudflare-d1-migration-maker.md) | Cloudflare Edge | Generates forward SQLite DDL migrations from TypeScript entity diffs | 338 tokens |
| [`conventional-committer`](catalog/conventional-committer.md) | Git Engineering | Synthesizes Conventional Commit messages from `git diff --stat` | 273 tokens |
| [`unit-test-synthesizer`](catalog/unit-test-synthesizer.md) | Testing / QA | Synthesizes happy-path, boundary, and error tests for a single function | 328 tokens |
| [`c2rust-function-porter`](catalog/c2rust-function-porter.md) | Code Porting | Transpiles isolated C++/C#/Python functions into idiomatic safe Rust | 351 tokens |
| [`c2rust-test-porter`](catalog/c2rust-test-porter.md) | Code Porting | Converts GoogleTest/Catch2/pytest test suites to standard `#[test]` Rust | 326 tokens |
| [`c2rust-type-scaffolder`](catalog/c2rust-type-scaffolder.md) | Code Porting | Maps C++ structs, enums, and smart pointers to idiomatic Rust types | 345 tokens |
| [`c2rust-crate-mapper`](catalog/c2rust-crate-mapper.md) | Code Porting | Maps C++ `#include` headers to modern Rust crates with `Cargo.toml` lines | 321 tokens |
| [`cpp-oop-to-data-oriented`](catalog/cpp-oop-to-data-oriented.md) | Code Porting | Converts C++ OOP virtual class hierarchies into Rust Data-Oriented enums | 432 tokens |
| [`rustc-error-burn-down`](catalog/rustc-error-burn-down.md) | Code Porting | Generates surgical 1-line patches for specific `rustc` diagnostic errors | 343 tokens |
| [`ast-refactor-transformer`](catalog/ast-refactor-transformer.md) | Refactoring | Replaces deprecated API patterns with modern idioms | 171 tokens |
| [`schema-validator`](catalog/schema-validator.md) | Data Quality | Heals corrupted or truncated JSON/YAML payloads | 157 tokens |


---

## 🔍 Continuous Discovery: Identifying Candidates Across Projects

While working in any repository (`~/PROJECTS`), proactively scan for operations that can be codified into micro-agents. 

### The 4-Filter Discovery Heuristic:
1. **Bounded Context**: Can the input payload be trimmed to $< 2,000$ tokens without losing critical context?
2. **Single-Shot**: Can the task be solved in exactly **one model turn** without conversational back-and-forth?
3. **Deterministic Output**: Can the output format be specified as a rigid patch, JSON object, or short text block?
4. **Repetitive Velocity**: Will this operation occur frequently across repos (e.g. fixing borrow-checker errors, writing release notes, generating mock data)?

**Action**: When all 4 criteria are met, create a new specification in `skills/micro-agent/catalog/<name>.md`.

---

## ⚡ Integration with `apfel-rs` and `zev-rs`

On Apple Silicon machines:
1. **Stage 0 (`zev-rs`)**: Ultra-fast calibrated probabilistic routing in **5.8 microseconds** with zero tokens.
2. **Stage 1 (`apfel-rs` Micro-Agent + Verification Harness)**: On-device execution via Apple FoundationModels / CoreML in **< 100 milliseconds** within the 4k-token budget. Deterministic harness checks output (AST, compiler, regex, schema); if valid, commit immediately.
3. **Stage 2 (Frontier Subagent)**: Escalate to Claude / Gemini only when Stage 1 verification fails or when multi-file repo synthesis exceeds 4,000 tokens.

Read [`references/apfel_integration.md`](references/apfel_integration.md) for concrete Rust/Swift bridging code.

---

## 🛠️ Step-by-Step: How to Build a New Micro-Agent

1. **Define the Single Responsibility**: State exactly one input type and one output type.
2. **Write the Lean System Prompt**: Use [`templates/micro_agent_prompt.md`](templates/micro_agent_prompt.md) to keep it under 200 tokens.
3. **Establish Input Pruning Rules**: Define how the caller extracts only the relevant lines (e.g. `sed`, AST parser, compiler error regex).
4. **Validate Token Budget**: Run the token counter utility:
   ```bash
   python3 skills/micro-agent/scripts/token_counter.py \
     --system prompt.md \
     --input sample_input.txt \
     --output sample_output.txt
   ```
5. **Define Deterministic Verification Harness**: Specify the automated validator engine (`syn`, `cargo check`, `serde_json`, regex, in-memory SQLite) and clear pass/escalation criteria.
6. **Publish to Catalog**: Commit the new micro-agent to `skills/micro-agent/catalog/`.

