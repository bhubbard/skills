# Micro-Agent: `c2rust-crate-mapper`

- **Domain**: Rust Dependency Mapping & Porting
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~480 tokens (System: 100, Input: 180, Output: 200)

---

## System Prompt
```text
You are an expert Rust ecosystem dependency mapper.
Given a list of C++, C#, GDScript, or Python library imports/includes and CMake dependencies, map them to modern, battle-tested idiomatic Rust crates.
Rules:
1. Recommend modern, maintained crates (e.g., `glam` over `cgmath`, `tracing` over `log`, `serde_json`, `rayon`, `clap`).
2. Output ONLY the suggested Cargo.toml dependency table and brief rust import aliases. No conversational prose.
```

---

## Input Schema
```text
INCLUDES / DEPENDENCIES:
#include <glm/glm.hpp>
#include <glm/gtc/quaternion.hpp>
#include <nlohmann/json.hpp>
#include <spdlog/spdlog.h>
#include <tbb/parallel_for.h>
```

---

## Output Contract
```toml
[dependencies]
glam = { version = "0.29", features = ["serde"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
rayon = "1.10"
```

```rust
// Mappings:
// glm::vec3 -> glam::Vec3, glm::quat -> glam::Quat
// nlohmann::json -> serde_json::Value
// spdlog::info!() -> tracing::info!()
// tbb::parallel_for -> rayon::iter::IntoParallelIterator
```

---

## Verification Harness
- **Validator Engine**: `toml::from_str` Validator
- **Verification Rule**:
  1. Parse output snippet with a TOML parser.
  2. Verify all mapped crates exist and specify valid version constraints or features (e.g. `serde = { version = "1.0", features = ["derive"] }`).
- **Pass Criteria**: Clean TOML parse with recognized crate names.
- **Escalation Action**: If crate mapping is ambiguous or TOML is invalid, escalate to Tier 2.
