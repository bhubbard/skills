# Code Porting Skills

Twelve skills for porting and rewriting large codebases from one language to another, distilled from Bun's Zig→Rust rewrite (~535k lines, 11 days, Claude Code + adversarial review — see [bun.com/blog/bun-in-rust](https://bun.com/blog/bun-in-rust)) and generalized to any language pair.

Seven skills are **generic** (any port); five are **Rust-specific** (target = Rust).

## Generic porting

| Skill | Use when |
|---|---|
| `port-planning` | At the very start — incremental vs. big-bang, PORTING.md, trial run |
| `porting-workflow-loops` | Executing the port — parallel write→review→apply loops, git/worktree discipline |
| `adversarial-code-review` | Reviewing a big/AI-generated diff — reviewer sees only the diff, hunts bugs |
| `compiler-errors-as-work-queue` | Thousands of build errors after a port/refactor — parallelize the burndown |
| `test-suite-driven-port` | Verifying correctness — reuse the original suite, smoke → local → CI green |
| `semantic-porting-pitfalls` | Avoiding "looks identical, behaves differently" regressions (any language) |
| `port-verification-checklist` | Final gate before merge — confirm the green is real, nothing stubbed |

## Rust-specific porting

| Skill | Use when |
|---|---|
| `port-to-rust-playbook` | Entry point when the target is Rust — why Rust, and the full sequence |
| `rust-lifetimes-analysis` | Adding lifetimes/ownership to manual-memory or GC'd code — LIFETIMES.tsv |
| `zig-to-rust-mapping` | Construct-by-construct translation reference — feeds PORTING.md |
| `rust-crate-decomposition` | Splitting one giant crate into ~100 — avoid cyclic dependencies |
| `rust-porting-mistakes` | Real Rust-target regressions — debug_assert!, bounds checks, bytemuck, comptime |

## Typical flow

```
port-planning
  └─ zig-to-rust-mapping (build PORTING.md)      [Rust target]
  └─ rust-lifetimes-analysis (build LIFETIMES.tsv) [Rust target]
porting-workflow-loops (translate in parallel)
  └─ adversarial-code-review (every change)
rust-crate-decomposition (split crates)          [Rust target]
compiler-errors-as-work-queue (burn down errors)
test-suite-driven-port (smoke → local → CI green)
  └─ semantic-porting-pitfalls / rust-porting-mistakes (watch for traps)
port-verification-checklist (verify, then merge)
```

## Source

- Bun blog: [Rewriting Bun in Rust](https://bun.com/blog/bun-in-rust)
- The methodology (dynamic workflows + adversarial review) and the specific bug examples are drawn from that write-up.
