# Micro-Agent: `unit-test-synthesizer`

- **Domain**: Software Testing & Quality Assurance
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~850 tokens (System: 140, Input: 360, Output: 350)

---

## System Prompt
```text
You are an automated unit test synthesizer for Rust and TypeScript.
Given a single pure function definition, generate exactly 3 focused unit tests covering:
1. Standard happy path
2. Boundary / edge condition (zero, empty, max value, or overflow)
3. Error / invalid input condition

Output ONLY executable test code inside a markdown code block. Do NOT include explanations.
```

---

## Input Schema
```rust
pub fn calculate_aspect_ratio(width: u32, height: u32) -> Result<f32, String> {
    if width == 0 || height == 0 {
        return Err("Dimensions must be non-zero".to_string());
    }
    Ok(width as f32 / height as f32)
}
```

---

## Output Contract
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_aspect_ratio_standard_16_9() {
        let ratio = calculate_aspect_ratio(1920, 1080).unwrap();
        assert!((ratio - 1.7777778).abs() < 1e-4);
    }

    #[test]
    fn test_aspect_ratio_square_1_1() {
        let ratio = calculate_aspect_ratio(1024, 1024).unwrap();
        assert_eq!(ratio, 1.0);
    }

    #[test]
    fn test_aspect_ratio_zero_dimension_error() {
        assert!(calculate_aspect_ratio(0, 1080).is_err());
        assert!(calculate_aspect_ratio(1920, 0).is_err());
    }
}
```

---

## Verification Harness
- **Validator Engine**: `cargo test` / `vitest` Isolated Runner
- **Verification Rule**:
  1. Inject generated unit tests alongside target function in a sandbox buffer.
  2. Run `cargo test` (Rust) or `vitest run` (TypeScript).
  3. Verify all 3 generated tests (happy path, boundary, error) execute and evaluate to true.
- **Pass Criteria**: Generated test suite compiles and passes 100% of assertions against the pure function.
- **Escalation Action**: If test suite fails to compile or assertions fail on correct logic, escalate to Tier 2.
