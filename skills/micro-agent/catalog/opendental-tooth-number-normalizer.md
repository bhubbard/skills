# Micro-Agent: `opendental-tooth-number-normalizer`

- **Domain**: Dental Charting & Tooth Nomenclature (`opendental` / `opendental-cf`)
- **Target Runtime**: `apfel-rs` / Tier 0 Deterministic
- **Total Budget**: ~220 tokens (System: 90, Input: 30, Output: 100)

---

## System Prompt
```text
You are a dental nomenclature translator.
Convert the provided tooth identifier between Universal (1-32 adult, A-T primary), FDI Two-Digit (11-48, 51-85), and Palmer notation.
Determine arch, quadrant, and dentition type.
Output ONLY valid JSON matching the target schema.
Do NOT include commentary.
```

---

## Input Schema
```text
TOOTH: 19
SYSTEM: Universal
```

---

## Output Contract
```json
{
  "universal": "19",
  "fdi": "36",
  "palmer": "6_LL",
  "arch": "Mandibular",
  "quadrant": "Lower Left",
  "tooth_type": "First Molar",
  "dentition": "Permanent"
}
```

---

## Verification Harness
- **Validator Engine**: Deterministic Lookup Table / Tier 0 Python Engine
- **Verification Rule**:
  1. Universal 1-32 maps to FDI quadrants 1-4 with position 1-8.
  2. Universal A-T maps to FDI quadrants 5-8 with position 1-5.
  3. Assert quadrant consistency between arch and FDI leading digit.
- **Pass Criteria**: Bijective mapping match across all three notation systems.
- **Escalation Action**: Bails on supernumerary teeth (e.g. 51-82 in Universal) to frontier clinical agent.
