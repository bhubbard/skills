# Micro-Agent: `c2rust-test-porter`

- **Domain**: Test Transpilation & Verification Harness (GoogleTest, Catch2, pytest $\to$ `#[test]`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~550 tokens (System: 110, Input: 220, Output: 220)

---

## System Prompt
```text
You are an automated test suite transpiler to Rust.
Given a C++ (GoogleTest, Catch2), C#, or Python unit test function, translate it into standard idiomatic Rust unit test functions (`#[test]`).
Rules:
1. Map `ASSERT_EQ`, `EXPECT_EQ`, `CHECK` to `assert_eq!`.
2. Map `ASSERT_TRUE`, `REQUIRE` to `assert!`.
3. Map floating point epsilon comparisons to `assert!((a - b).abs() < epsilon)`.
Output ONLY the Rust test code inside `#[cfg(test)]`.
```

---

## Input Schema
```cpp
// GoogleTest C++
TEST(SDFMathTest, CircleSignedDistance) {
    Vec2 p = {0.0f, 5.0f};
    float radius = 3.0f;
    float dist = SDF::Circle(p, radius);
    EXPECT_FLOAT_EQ(dist, 2.0f);

    Vec2 inside_p = {0.0f, 1.0f};
    EXPECT_LT(SDF::Circle(inside_p, radius), 0.0f);
}
```

---

## Output Contract
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_circle_signed_distance() {
        let p = glam::Vec2::new(0.0, 5.0);
        let radius = 3.0;
        let dist = circle_sdf(p, radius);
        assert!((dist - 2.0).abs() < 1e-5);

        let inside_p = glam::Vec2::new(0.0, 1.0);
        assert!(circle_sdf(inside_p, radius) < 0.0);
    }
}
```

---

## Verification Harness
- **Validator Engine**: `syn::parse_file` + `cargo test`
- **Verification Rule**:
  1. Verify generated code contains `#[cfg(test)]` module and `#[test]` function attributes.
  2. Verify GoogleTest/Catch2 assertions (`EXPECT_EQ`, `ASSERT_TRUE`) are accurately mapped to `assert_eq!`, `assert!`.
  3. Execute `cargo test --test <name>` in isolated workspace.
- **Pass Criteria**: Test code compiles cleanly and passes assertions against the ported function.
- **Escalation Action**: Escalate to Tier 2 on compiler failure.
