# Micro-Agent: `cpp-oop-to-data-oriented`

- **Domain**: Architecture Refactoring (OOP to Data-Oriented Rust)
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~720 tokens (System: 120, Input: 300, Output: 300)

---

## System Prompt
```text
You are an expert systems programmer specializing in converting C++ OOP class hierarchies to idiomatic Rust Data-Oriented Design (DOD).
Rules:
1. Avoid `Arc<Mutex<dyn Trait>>` or deep inheritance trees where closed enums or component arrays work better.
2. If types represent discrete variants, use a tagged `enum`.
3. If entities have dynamic compositions, propose flat component structs or handle IDs.
4. Output ONLY the Rust enum/struct definitions and dispatch implementation. No conversational prose.
```

---

## Input Schema
```cpp
class Entity {
public:
    virtual ~Entity() = default;
    virtual void Update(float dt) = 0;
    virtual void Render() const = 0;
};

class Player : public Entity {
    Vector3 position;
    float health;
public:
    void Update(float dt) override;
    void Render() const override;
};

class Projectile : public Entity {
    Vector3 velocity;
    float ttl;
public:
    void Update(float dt) override;
    void Render() const override;
};
```

---

## Output Contract
```rust
use glam::Vec3;

#[derive(Debug, Clone, PartialEq)]
pub enum EntityKind {
    Player { position: Vec3, health: f32 },
    Projectile { velocity: Vec3, ttl: f32 },
}

pub struct Entity {
    pub id: u64,
    pub kind: EntityKind,
}

impl Entity {
    pub fn update(&mut self, dt: f32) {
        match &mut self.kind {
            EntityKind::Player { position, .. } => {
                // Player physics update
            }
            EntityKind::Projectile { velocity, ttl } => {
                *ttl -= dt;
            }
        }
    }
}
```

---

## Verification Harness
- **Validator Engine**: `syn::parse_file` Layout Inspector
- **Verification Rule**:
  1. Parse output into valid Rust AST.
  2. Inspect struct fields: assert that data is stored in contiguous collections (`Vec<T>`, `Box<[T]>`) rather than pointer graphs or inheritance shims.
- **Pass Criteria**: Syntactically valid Rust adhering to Struct-of-Arrays (SoA) layout.
- **Escalation Action**: Escalate to Tier 2 on architectural failure.
