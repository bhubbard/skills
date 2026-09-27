# Grammar-Guided Decoding & Logit Masking Guide

> **Core Axiom**: Small Language Models (1B–3B) should **never** be allowed to generate free-form structured output. Free-form text generation guarantees syntax drift, missing braces, and hallucinations. **Logit masking makes syntax errors mathematically impossible.**

---

## 🔬 How Grammar-Guided Sampling Works

During autoregressive generation, at each token step $t$, the language model produces unnormalized logits over the vocabulary:
$$\mathbf{z}_t \in \mathbb{R}^{|V|}$$

Without constraints, the model samples from the full softmax distribution:
$$P(w_i) = \frac{e^{z_{t, i}}}{\sum_j e^{z_{t, j}}}$$

Under **Grammar-Guided Decoding** (GBNF / JSON Schema):
1. A deterministic context-free grammar (or state machine) tracks the parser state of the generated output so far.
2. At step $t$, the grammar identifies the exact subset of tokens $V_{\text{valid}} \subseteq V$ that can legally continue the sequence according to the target schema.
3. Tokens outside $V_{\text{valid}}$ have their logits masked to negative infinity ($-\infty$):
   $$\tilde{z}_{t, i} = \begin{cases} z_{t, i} & \text{if } w_i \in V_{\text{valid}} \\ -\infty & \text{otherwise} \end{cases}$$
4. The model physically **cannot** emit a token that breaks the JSON syntax, produces a trailing comma, or adds conversational filler (*"Sure! Here is the JSON:"*).

```
Model Logits ──► [ Grammar Masking Engine ] ──► Filtered Logits (Illegal Tokens = -Inf) ──► 100% Valid JSON
```

---

## 🛠️ Implementation Across Engines

### 1. `apfel-rs` (Apple FoundationModels / CoreML)
In `apfel-rs`, pass the JSON Schema directly to the inference options:

```rust
use apfel_rs::{Model, GenerateOptions, JsonSchema};

let schema = serde_json::json!({
    "type": "object",
    "properties": {
        "lead_id": { "type": "integer" },
        "status": { "type": "string" },
        "phone": { "type": "string" }
    },
    "required": ["lead_id", "status", "phone"],
    "additionalProperties": false
});

let options = GenerateOptions::builder()
    .temperature(0.0)
    .max_tokens(500)
    .json_schema(schema) // Activates CoreML token logit constraint mask
    .build();

let output = model.generate(&prompt, options)?;
// Output is guaranteed to deserialize cleanly into your Rust struct
let lead: LeadSummary = serde_json::from_str(&output)?;
```

---

### 2. `mlx-lm` (Apple Silicon Metal)
In `mlx-lm`, use Outlines or regex/schema logits processors:

```python
from mlx_lm import load, generate
from mlx_lm.sample_utils import make_grammar_processor

model, tokenizer = load("mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit")

schema = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["ok", "mismatch"]},
        "missing": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["status", "missing"]
}

# Constructs logit bias mask
logits_processor = make_grammar_processor(tokenizer, json_schema=schema)

response = generate(
    model, 
    tokenizer, 
    prompt=prompt, 
    logits_processors=[logits_processor],
    max_tokens=300
)
```

---

### 3. GBNF Grammars (`llama.cpp` / local engines)
For GBNF-compatible engines, use the canonical GBNF grammar definition:

```gbnf
root   ::= object
object ::= "{" ws ( pair ( "," ws pair )* )? "}"
pair   ::= string ":" ws value
value  ::= string | number | object | array | "true" | "false" | "null"
string ::= "\"" ([^"\\] | "\\" ["\\/bfnrt])* "\""
number ::= "-"? [0-9]+ ("." [0-9]+)?
array  ::= "[" ws ( value ( "," ws value )* )? "]"
ws     ::= [ \t\n\r]*
```

---

## 📋 Architectural Policy for Micro-Agents

1. **Every JSON Micro-Agent MUST have a companion JSON Schema**.
2. **Temperature must strictly be 0.0** (deterministic greedy decoding).
3. **Conversational tokens must be pruned from the prompt**; never ask the model to "be polite" or "explain why".
