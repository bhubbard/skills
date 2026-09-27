# Apple Silicon & `apfel-rs` Integration Guide

[`apfel-rs`](https://crates.io/crates/apfel-rs) is a native Rust library that interfaces directly with Apple Intelligence FoundationModels, CoreML, and Apple Silicon unified memory without requiring Python, PyTorch, or external cloud API calls.

Micro-agents are designed to be first-class citizens in `apfel-rs`.

---

## 🏎️ Why `apfel-rs` + Micro-Agents?

1. **Zero Network Latency**: Runs entirely on the Apple Neural Engine (ANE) and unified memory. Time-to-first-token is $< 20\text{ms}$.
2. **Deterministic Context**: Apple Intelligence models are trained and calibrated for compact context windows (typically 2,048 – 4,096 tokens). Staying under 4,000 tokens guarantees optimal attention fidelity without context degradation.
3. **Zero Financial Cost**: Local execution eliminates API token fees. You can execute tens of thousands of micro-agent invocations per day for free.
4. **Air-Gapped Privacy**: Sensitive codebases, API credentials, and internal proprietary logic never leave the local Mac.

---

## 🦀 Rust Implementation Pattern

Here is the canonical pattern for invoking a micro-agent using `apfel-rs` in a Rust CLI or daemon:

```rust
use apfel::{FoundationModel, GenerationConfig};
use anyhow::Result;

pub struct MicroAgentRunner {
    model: FoundationModel,
}

impl MicroAgentRunner {
    pub fn new() -> Result<Self> {
        let model = FoundationModel::load_default()?;
        Ok(Self { model })
    }

    pub fn execute(&self, system_prompt: &str, payload: &str) -> Result<String> {
        // Enforce 4,000 token budget envelope
        let total_chars = system_prompt.len() + payload.len();
        if total_chars > 12_000 {
            anyhow::bail!("Payload exceeds safe 4,000 token micro-agent budget (chars: {})", total_chars);
        }

        let prompt = format!(
            "<|system|>\n{}\n<|user|>\n{}\n<|assistant|>\n",
            system_prompt.trim(),
            payload.trim()
        );

        let config = GenerationConfig {
            max_tokens: 1024,
            temperature: 0.1, // Near-zero temperature for deterministic code fixes
            top_p: 0.9,
            stop_sequences: vec!["<|end|>".to_string(), "<|user|>".to_string()],
        };

        let response = self.model.generate(&prompt, &config)?;
        Ok(response.trim().to_string())
    }
}
```

---

## ⚡ Cascading: `zev-rs` $\to$ `apfel-rs` Micro-Agent

Combine `zev-rs` and `apfel-rs` into an ultra-low-latency pipeline:

1. **Step 1: Zero-Token Pre-Filter (`zev-rs`)**:
   - `zev-rs` evaluates the AST or input in **5.8 microseconds** with zero tokens.
   - Example: Determine if a compiler error is a simple lifetime/borrow issue, missing import, or complex architectural error.
2. **Step 2: Micro-Agent Execution (`apfel-rs`)**:
   - If classified as a syntax or borrow-check fix, dispatch to the `rust-compiler-healer` micro-agent running on `apfel-rs` (~60ms).
3. **Step 3: Escalation (Frontier LLM)**:
   - Only escalate if `zev-rs` flags high entropy or if the micro-agent output fails verification (`cargo check` fails).
