# Micro-Agent: `timesfm-forecast-patch-tokenizer`

- **Domain**: Time-Series Foundation Models (`timesfm-rs`)
- **Target Runtime**: `apfel-rs` (Apple FoundationModels) / Local SLM
- **Total Budget**: ~290 tokens (System: 100, Input: 60, Output: 130)

---

## System Prompt
```text
You are a time-series foundation model patch tokenizer.
Given raw historical timestamp/value pairs, infer the series frequency (hourly, daily, weekly), normalize values via z-score (subtract mean, divide by standard deviation), and package into fixed-size 32-value patch vectors for model inference.
Output ONLY valid JSON.
```

---

## Input Schema
```text
SERIES: [120.5, 122.0, 119.8, 124.5, 128.2, 131.0, 129.4, 135.2]
TIMESTAMPS: ["2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08"]
TARGET_PATCH_LEN: 8
```

---

## Output Contract
```json
{
  "frequency": "daily",
  "mean": 126.325,
  "std": 5.485,
  "normalized_patch": [-1.062, -0.789, -1.189, -0.333, 0.342, 0.852, 0.561, 1.618],
  "patch_length": 8,
  "is_stationary": false
}
```

---

## Verification Harness
- **Validator Engine**: Numerical Array Validator (`numpy` / `serde_json`)
- **Verification Rule**:
  1. `normalized_patch` length must equal input series length.
  2. Mean of `normalized_patch` must be within $[-0.05, 0.05]$ (zero mean after normalization).
  3. Standard deviation of `normalized_patch` must be within $[0.95, 1.05]$.
- **Pass Criteria**: Standardized normalized vector ready for transformer context ingestion.
- **Escalation Action**: If standard deviation is 0 (constant series), set normalized patch to array of zeros.
