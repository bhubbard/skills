# Micro-Agent: `ast-refactor-transformer`

- **Domain**: Refactoring & AST Transformations
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~350 tokens (System: 100, Input: 180, Output: 70)

---

## System Prompt
```text
You are an AST code refactoring transformer.
Given an original code snippet and a replacement pattern directive, output ONLY the transformed replacement code.
Do not provide commentary, explanations, or markdown fences. Output plain raw code.
```

---

## Input Schema
```text
DIRECTIVE:
Replace deprecated `std::sync::mpsc::channel` with `tokio::sync::mpsc::channel(100)`

SOURCE:
let (tx, rx) = std::sync::mpsc::channel();
```

---

## Output Contract
```rust
let (tx, mut rx) = tokio::sync::mpsc::channel(100);
```

---

## Verification Harness
- **Validator Engine**: AST Parser (`syn` for Rust / `oxc` for JS/TS)
- **Verification Rule**:
  1. Output must parse into a valid AST node without syntax errors.
  2. AST diff boundary verification: only the targeted symbol or call site is transformed; parent and sibling AST tokens remain byte-identical.
- **Pass Criteria**: AST parses cleanly with zero diagnostic errors and passes scope boundary check.
- **Escalation Action**: Reject patch immediately on parse error and escalate to Tier 2 (Claude / Gemini).
