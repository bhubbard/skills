# AST-Hydrated Slicing: Eliminating Context Blindness

> **The Problem**: Giving a code-repair micro-agent only a 15-line blind window forces it to guess external types and lifetimes, inevitably leading to naive band-aids (e.g. slapping `.clone()` everywhere or wrapping in `Arc<Mutex<T>>`).

---

## 🏛️ The Dependency Triad Architecture

To fix context blindness while remaining within the **4,000-token envelope**, callers MUST NOT pass raw arbitrary line numbers. Instead, extract an **AST-Hydrated Dependency Triad**:

```
┌────────────────────────────────────────────────────────┐
│                   The Dependency Triad                 │
├────────────────────────────┬───────────────────────────┤
│ 1. The Diagnostic Payload  │ rustc/tsc JSON error span │
├────────────────────────────┼───────────────────────────┤
│ 2. The Call Site AST       │ Complete enclosing fn     │
├────────────────────────────┼───────────────────────────┤
│ 3. The Definition Site AST │ Struct / Trait signature  │
└────────────────────────────┴───────────────────────────┘
```

---

### Triad Extraction Protocol

#### 1. Extract The Diagnostic Payload
Parse the machine-readable compiler stderr (`cargo check --message-format=json` or `tsc --pretty false`):
- Error code (e.g., `E0382`, `E0502`, `E0061`).
- Exact line, column, and span label (*"borrow of `x` occurs here"*).

#### 2. Extract The Call Site (Enclosing Function AST)
Using an AST tool (such as `tree-sitter-rust`, `syn`, or regex AST block matchers), isolate the enclosing function:
```rust
// Slice 2: Call Site
pub fn process_message(&mut self, msg: Message) -> Result<()> {
    let payload = msg.into_payload();
    self.router.route(&payload)?; // <--- Error: cannot borrow *self as mutable
    self.history.push(payload);
    Ok(())
}
```

#### 3. Extract The Target Definition (Declaration AST)
Locate the definition of the struct, trait, or method involved in the diagnostic:
```rust
// Slice 3: Target Definition
pub trait MessageRouter {
    fn route(&mut self, payload: &Payload) -> Result<()>;
}
```

---

## 🚨 The Cross-Boundary Escape Hatch

Micro-agents are strictly forbidden from guessing architecture. If a diagnostic crosses systemic boundaries, **do not execute the micro-agent**.

### The 4 Auto-Escalation Triggers:
1. **Multi-File Spread**: The error diagnostic spans $>2$ distinct files.
2. **Trait Implementation Split**: The error involves a trait defined in an external crate where the orphan rule or lifetime parameters apply.
3. **Macro Expansion**: The diagnostic points into the guts of a complex procedural macro expansion.
4. **Architectural Lifetime Restructuring**: Resolving the error requires changing function signatures across a public API.

When an auto-escalation trigger fires, the pipeline immediately returns:
```json
{
  "action": "escalate",
  "reason": "MULTI_FILE_LIFETIME_BOUNDARY",
  "target_agent": "frontier_workspace_agent"
}
```

This prevents micro-agents from degrading code quality with hacky `.clone()` patches and ensures global architectural reasoning is handled by the frontier model.
