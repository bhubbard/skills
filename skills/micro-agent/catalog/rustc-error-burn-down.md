# Micro-Agent: `rustc-error-burn-down`

- **Domain**: Automated Compiler Error Resolution & Transpilation Burn-Down
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~680 tokens (System: 120, Input: 280, Output: 280)

---

## System Prompt
```text
You are an expert Rust compiler error repair assistant.
Given a single rustc diagnostic error message (from cargo check --message-format=json or terminal) and the snippet of code causing it, output the surgical fix.
Rules:
1. Target the exact compiler diagnostic code (e.g. E0308, E0425, E0599, E0277).
2. Prefer minimal, clean Rust fixes (e.g. adding `.into()`, `.as_str()`, borrowing `&`, dereferencing `*`, or implementing missing trait).
3. Output ONLY the corrected Rust code block or replacement chunk. No conversational prose.
```

---

## Input Schema
```text
ERROR DIAGNOSTIC:
error[E0308]: mismatched types
  --> src/renderer.rs:42:31
   |
42 |     render_target.bind_texture(texture_name);
   |                   ------------ ^^^^^^^^^^^^ expected `&str`, found `String`
   |                   |
   |                   arguments to this method are incorrect

CODE SNIPPET:
pub fn setup_pipeline(render_target: &mut RenderTarget, texture_name: String) {
    render_target.bind_texture(texture_name);
}
```

---

## Output Contract
```rust
pub fn setup_pipeline(render_target: &mut RenderTarget, texture_name: &str) {
    render_target.bind_texture(texture_name);
}
```
*(or calling `render_target.bind_texture(&texture_name);` if signature cannot change)*

---

## Verification Harness
- **Validator Engine**: Compiler Diagnostic Counter
- **Verification Rule**:
  1. Measure baseline compiler error count: `N_pre = count(cargo check errors)`.
  2. Apply candidate patch.
  3. Measure updated compiler error count: `N_post = count(cargo check errors)`.
  4. Assert: `N_post < N_pre`.
- **Pass Criteria**: Error burn-down invariant satisfied (`N_post < N_pre`).
- **Escalation Action**: If `N_post >= N_pre`, immediately revert patch and escalate to Tier 2.
