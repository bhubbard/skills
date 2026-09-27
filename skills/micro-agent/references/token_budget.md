# Token Budget & Context Pruning Specification

To guarantee that small on-device models (`apfel-rs`, Gemini Nano, Llama 3.2 1B/3B) never fail, truncate, or experience attention degradation, micro-agents strictly enforce the **4K Token Envelope**.

---

## 📊 The 4,000-Token Allocation

```
[============================= 4,000 Tokens Max =============================]
[ System Prompt: 250 ] [ Payload: 2,250 ] [ Tool: 200 ] [ Output Budget: 1,300 ]
```

### 1. System Prompt ($\le 250$ tokens)
- Zero conversational pleasantries.
- Zero persona roleplay ("You are a world-class senior engineer...").
- Exact input format specification.
- Exact output format schema.
- Example:
  ```text
  You are an automated compiler healer. Given a compiler diagnostic and code snippet, output ONLY the corrected lines inside a ```diff block. Do not explain.
  ```

### 2. Tool Schema ($\le 200$ tokens)
- Most micro-agents should have **zero tools** (pure string $\to$ string or string $\to$ JSON).
- If a tool is necessary, provide at most **one** tool with a compact JSON Schema:
  ```json
  {
    "name": "apply_patch",
    "description": "Applies replacement code to target file",
    "parameters": {
      "type": "object",
      "properties": {
        "start_line": { "type": "integer" },
        "end_line": { "type": "integer" },
        "replacement": { "type": "string" }
      },
      "required": ["start_line", "end_line", "replacement"]
    }
  }
  ```

### 3. Input Payload ($\le 2,250$ tokens)
- **Do not send entire files.** A 400-line file easily consumes 3,000+ tokens.
- **Context Pruning Rules**:
  - For compiler errors: extract the exact diagnostic lines + 15 lines before and after the offending line.
  - For function tests: extract only the target function signature and docstring.
  - For git commits: run `git diff --stat` + `git diff --unified=2` capped to 100 lines.

### 4. Output Generation ($\le 1,300$ tokens)
- Pre-allocated completion headroom.
- If output exceeds 1,300 tokens, the task is too broad and must be split into multiple micro-agent passes.

---

## 🧮 Token Density Heuristics

- **Code (Rust/TypeScript/Python)**: $\approx 1 \text{ token per } 3.2 \text{ characters}$ (dense due to syntax tokens, braces, symbols).
- **English Prose**: $\approx 1 \text{ token per } 4 \text{ characters}$.
- **Stack Traces / Compiler Diagnostics**: $\approx 1 \text{ token per } 2.8 \text{ characters}$.

A 2,250-token input payload corresponds to approximately **7,000 characters** or roughly **120 lines of code**.
