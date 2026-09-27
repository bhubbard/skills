# Micro-Agent: `natural-to-awk`

- **Domain**: CLI Automation, Log Processing & Text Extraction (`apfel-awk`)
- **Target Runtime**: `apfel-rs` / Local SLM
- **Total Budget**: ~220 tokens (System: 90, Input: 80, Output: 50)

---

## System Prompt
```text
You are an expert Unix `awk` and text stream filter synthesizer.
Given a sample log line and a plain-English extraction request, output ONLY the single-line `awk` command.
Do not provide shell commentary, markdown formatting, or explanations.
```

---

## Input Schema
```text
SAMPLE LOG:
2026-09-26 21:40:12 192.168.1.45 POST /api/v1/infer 502 124ms

REQUEST:
Print the IP address (column 3) and latency (column 7) for all requests with status code >= 500 (column 6).
```

---

## Output Contract
```bash
awk '$6 >= 500 { print $3, $7 }'
```

---

## Verification Harness
- **Validator Engine**: GNU awk Lint Validator
- **Verification Rule**:
  1. Validate awk syntax:
     `awk --lint -f - /dev/null <<< "$OUTPUT"`
  2. Verify command exit code is 0.
- **Pass Criteria**: Output is valid, lint-clean `awk` code.
- **Escalation Action**: Escalate to Tier 2 on syntax error.
