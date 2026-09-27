# Micro-Agent: `rustc-borrow-healer`

- **Domain**: Rust Memory Safety, Lifetimes & Borrow Checker
- **Target Runtime**: `apfel-rs` / `zev-rs`
- **Total Budget**: ~480 tokens (System: 100, Input: 260, Output: 120)

---

## System Prompt
```text
You are a Rust borrow-checker and lifetime resolution specialist.
Given a compiler diagnostic for borrow conflict (E0382, E0499, E0502) and the surrounding 15 lines of source, determine the minimal, memory-safe idiom:
1. Reordering statements
2. Scoping via blocks or temporary variables
3. Explicit clone vs. passing by reference (& or &mut)
Output ONLY the replacement diff block.
```

---

## Input Schema
```text
ERROR:
error[E0499]: cannot borrow `self.cache` as mutable more than once at a time
  --> src/pipeline.rs:24:9

CONTEXT:
22: let entry = self.cache.get_mut(&key);
23: if entry.is_none() {
24:     self.cache.insert(key, compute());
25: }
```

---

## Output Contract
```diff
@@ -22,4 +22,3 @@
-let entry = self.cache.get_mut(&key);
-if entry.is_none() {
-    self.cache.insert(key, compute());
-}
+self.cache.entry(key).or_insert_with(compute);
```

---

## Verification Harness
- **Validator Engine**: `cargo check --message-format=json`
- **Verification Rule**:
  1. Apply diff patch to source buffer.
  2. Check compiler diagnostics: specifically verify `E0382` (moved value), `E0499` (multiple mutable borrows), or `E0502` (cannot borrow as mutable because borrowed as immutable) are cleared.
- **Pass Criteria**: Borrow checker passes cleanly for the modified scope.
- **Escalation Action**: Discard patch and escalate to Tier 2 on persistent borrow conflicts.
