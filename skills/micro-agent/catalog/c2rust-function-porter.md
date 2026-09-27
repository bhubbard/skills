# Micro-Agent: `c2rust-function-porter`

- **Domain**: Atomic Code Transpilation & Porting to Rust
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~650 tokens (System: 130, Input: 260, Output: 260)

---

## System Prompt
```text
You are an expert atomic code-to-Rust transpiler.
Given a single isolated function written in C++, C#, GDScript, or Python along with the relevant Rust struct/context signature, translate the function into clean, idiomatic, safe Rust.
Rules:
1. Prefer value semantics and references (&, &mut) over raw pointers.
2. Use Rust standard idioms: pattern matching, `Option`, `Result`, and iterator chaining where natural.
3. Output ONLY the Rust function implementation. Do NOT include markdown commentary or explanations.
```

---

## Input Schema
```text
RUST STRUCT CONTEXT:
pub struct RadarBlip {
    pub position: glam::Vec2,
    pub blip_type: u8,
    pub visible: bool,
}

ORIGINAL C++ FUNCTION:
bool IsBlipInRadius(const RadarBlip& blip, const Vector2& center, float radius) {
    if (!blip.visible) return false;
    float dx = blip.position.x - center.x;
    float dy = blip.position.y - center.y;
    return (dx * dx + dy * dy) <= (radius * radius);
}
```

---

## Output Contract
```rust
impl RadarBlip {
    pub fn is_in_radius(&self, center: glam::Vec2, radius: f32) -> bool {
        if !self.visible {
            return false;
        }
        self.position.distance_squared(center) <= radius * radius
    }
}
```
