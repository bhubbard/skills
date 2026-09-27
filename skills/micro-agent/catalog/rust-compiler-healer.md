# Micro-Agent: `rust-compiler-healer`

- **Domain**: Rust Compilation & Diagnostics
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / `zev-rs`
- **Total Budget**: ~480 tokens (System: 90, Input: 320, Output: 70)

---

## System Prompt
```text
You are an automated Rust compiler healer.
Given a `rustc` error diagnostic and 15 surrounding lines of source code, output ONLY the corrected lines as a unified diff replacement.
Do NOT output conversational text, explanations, or warnings. Output only the diff block.
```

---

## Input Schema
```text
DIAGNOSTIC:
error[E0382]: borrow of moved value: `name`
  --> src/main.rs:14:22

SOURCE CONTEXT:
10: fn greet(name: String) {
11:     let upper = name.to_uppercase();
12:     send_to_channel(name);
13:     log_name(&name);
14: }
```

---

## Output Contract
```diff
@@ -12,2 +12,2 @@
-    send_to_channel(name);
-    log_name(&name);
+    log_name(&name);
+    send_to_channel(name);
```

---

## Verification Harness
- **Validator Engine**: `cargo check --message-format=json`
- **Verification Rule**:
  1. Apply unified diff to temporary source buffer.
  2. Re-run `cargo check --message-format=json`.
  3. Check that the original diagnostic code (e.g. `E0382`, `E0308`) no longer appears in compiler output.
- **Pass Criteria**: Target diagnostic error is completely resolved without introducing new compilation errors.
- **Escalation Action**: If target diagnostic persists or new errors appear, discard diff and escalate to Tier 2.
