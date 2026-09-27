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
- **Example**: [`catalog/rust-compiler-healer.md`](catalog/rust-compiler-healer.md) (~480 tokens total).

### 2. The Synthesizer (Tests & Documentation)
- **Role**: Takes an isolated struct/function signature and generates 3 edge-case tests or docstrings.
- **Output**: Code block with `#[test]` or standard doc comments.
- **Example**: [`catalog/unit-test-synthesizer.md`](catalog/unit-test-synthesizer.md) (~850 tokens total).

### 3. The Committer (Changelog & Commits)
- **Role**: Takes `git diff --stat` and key diff chunks; produces conventional commit message.
- **Output**: `feat(scope): concise summary` + 3 bullet points.
- **Example**: [`catalog/conventional-committer.md`](catalog/conventional-committer.md) (~600 tokens total).

### 4. The Transformer (AST & API Refactor)
- **Role**: Rewrites deprecated function calls or transforms one data structure into another.
- **Output**: Clean replacement code.
- **Example**: [`catalog/ast-refactor-transformer.md`](catalog/ast-refactor-transformer.md) (~350 tokens total).

### 5. The Schema Validator & Repairer
- **Role**: Takes malformed or incomplete JSON/YAML and repairs it to conform to a target schema.
- **Output**: Strictly valid JSON with zero conversational commentary.
- **Example**: [`catalog/schema-validator.md`](catalog/schema-validator.md) (~400 tokens total).

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
2. **Stage 1 (`apfel-rs` Micro-Agent)**: On-device execution via Apple FoundationModels / CoreML in **< 100 milliseconds** within the 4k-token budget.
3. **Stage 2 (Frontier Subagent)**: Only escalate to Claude 3.5 Sonnet or Gemini 1.5 Pro when multi-file repo synthesis exceeds 4,000 tokens.

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
5. **Publish to Catalog**: Commit the new micro-agent to `skills/micro-agent/catalog/`.
