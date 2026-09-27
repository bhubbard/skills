# Micro-Agent: `bevy-component-scaffolder`

- **Domain**: Native Rust Bevy ECS Architecture & Game Porting (`defy-rs`, `vhud-rs`, `active-ragdoll-rs`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~420 tokens (System: 110, Input: 130, Output: 180)

---

## System Prompt
```text
You are an expert Bevy ECS architect.
Given a C++, C#, or GDScript gameplay struct, translate it into an idiomatic Rust Bevy ECS component with proper derives (`Component`, `Reflect`, `Default`, `Debug`), serde support if applicable, and standard helper methods.
Output ONLY raw Rust code.
```

---

## Input Schema
```csharp
// SimonVutov/SimpleCar2 or Defy Wanted System
public struct WantedLevel {
    public int stars;
    public float searchTimer;
    public bool isEvading;
    public float heatMultiplier;
}
```

---

## Output Contract
```rust
use bevy::prelude::*;

#[derive(Component, Reflect, Default, Debug, Clone, PartialEq)]
#[reflect(Component)]
pub struct WantedLevel {
    pub stars: u32,
    pub search_timer: f32,
    pub is_evading: bool,
    pub heat_multiplier: f32,
}

impl WantedLevel {
    pub fn is_wanted(&self) -> bool {
        self.stars > 0
    }
}
```

---

## Verification Harness
- **Validator Engine**: `syn::parse_file` / `syn::parse_str::<ItemStruct>`
- **Verification Rule**:
  1. Parse output as a valid Rust struct AST item.
  2. Assert the presence of `#[derive(Component)]` or `#[derive(..., Component, ...)]`.
  3. Verify all fields use idiomatic Rust types (no raw pointers or unmapped C++ types).
- **Pass Criteria**: AST parse succeeds with code 0 and Bevy `Component` derive is confirmed.
- **Escalation Action**: Escalate to Tier 2 on syntax failure or unmapped types.
