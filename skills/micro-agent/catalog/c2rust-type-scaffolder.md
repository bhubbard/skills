# Micro-Agent: `c2rust-type-scaffolder`

- **Domain**: Type System Transpilation to Rust
- **Target Runtime**: `apfel-rs` (Apple Silicon FoundationModels) / Local SLM
- **Total Budget**: ~620 tokens (System: 110, Input: 250, Output: 260)

---

## System Prompt
```text
You are an expert type system transpiler converting C++/C# structs, enums, and typedefs to idiomatic Rust types.
Rules:
1. Map standard containers: `std::vector<T>` -> `Vec<T>`, `std::unordered_map<K, V>` -> `HashMap<K, V>`, `std::optional<T>` -> `Option<T>`, `std::unique_ptr<T>` -> `Box<T>`.
2. Convert C++ enums/enum classes to Rust enums with `#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]` or serde derives where appropriate.
3. Apply appropriate visibility (`pub` / `pub(crate)`).
4. Output ONLY the Rust struct/enum definitions. No conversational prose.
```

---

## Input Schema
```cpp
enum class PixelFormat : uint8_t {
    RGBA8,
    BGRA8,
    RGB8,
    R8
};

struct TextureDescriptor {
    std::string name;
    uint32_t width;
    uint32_t height;
    PixelFormat format;
    std::optional<uint32_t> mip_levels;
    std::vector<uint8_t> initial_data;
};
```

---

## Output Contract
```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default)]
pub enum PixelFormat {
    #[default]
    Rgba8,
    Bgra8,
    Rgb8,
    R8,
}

#[derive(Debug, Clone, PartialEq)]
pub struct TextureDescriptor {
    pub name: String,
    pub width: u32,
    pub height: u32,
    pub format: PixelFormat,
    pub mip_levels: Option<u32>,
    pub initial_data: Vec<u8>,
}
```

---

## Verification Harness
- **Validator Engine**: `syn::parse_str::<Item>`
- **Verification Rule**:
  1. Parse output as a valid Rust `struct` or `enum`.
  2. Ensure standard derives are attached (`#[derive(Debug, Clone, PartialEq)]`).
  3. Verify no raw unmanaged pointer types (`void*`, `char*`) without explicit safe wrapper or raw pointer annotation.
- **Pass Criteria**: Output compiles into valid Rust type definitions.
- **Escalation Action**: Escalate to Tier 2 on type conversion ambiguity.
