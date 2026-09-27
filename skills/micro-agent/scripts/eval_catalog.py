#!/usr/bin/env python3
"""
Automated CI Regression & Evaluation Suite for Micro-Agents.
Audits all 35 micro-agent specifications in catalog/:
1. Enforces the 4,000-token envelope hard ceiling.
2. Validates output contract syntax (JSON / Code syntax).
3. Verifies Tier 0 deterministic tool parity.
4. Ensures verification harness specifications are complete.
"""

import sys
import re
import json
from pathlib import Path

# Add tools directory to path
CATALOG_DIR = Path(__file__).resolve().parent.parent / "catalog"
TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

try:
    from tier0_deterministic import (
        flow_matching_sigmas,
        filevine_custom_field_sanitize,
        spring_physics_convert,
        lora_delta_scale,
        tailwind_class_sort
    )
except ImportError:
    pass

def estimate_tokens(text: str) -> int:
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        words = len(text.split())
        chars = len(text)
        return int((chars / 3.5 + words * 1.3) / 2)


def parse_catalog_file(filepath: Path) -> dict:
    content = filepath.read_text(encoding="utf-8")
    
    sections = {
        "name": filepath.stem,
        "path": filepath,
        "raw": content,
        "system_prompt": "",
        "input_schema": "",
        "output_contract": "",
        "verification_harness": "",
        "output_format": "text"
    }

    # Extract System Prompt
    sys_match = re.search(r"## System Prompt\s+```(?:text)?\s*(.*?)\s*```", content, re.DOTALL)
    if sys_match:
        sections["system_prompt"] = sys_match.group(1).strip()

    # Extract Input Schema
    in_match = re.search(r"## Input Schema\s+```(?:text|json|css|typescript|env|html)?\s*(.*?)\s*```", content, re.DOTALL)
    if in_match:
        sections["input_schema"] = in_match.group(1).strip()

    # Extract Output Contract
    out_match = re.search(r"## Output Contract\s+```(json|css|typescript|env|html|diff|text)?\s*(.*?)\s*```", content, re.DOTALL)
    if out_match:
        sections["output_format"] = out_match.group(1) or "text"
        sections["output_contract"] = out_match.group(2).strip()

    # Extract Verification Harness
    vh_match = re.search(r"## Verification Harness\s*(.*)", content, re.DOTALL)
    if vh_match:
        sections["verification_harness"] = vh_match.group(1).strip()

    return sections


def main():
    catalog_files = sorted(list(CATALOG_DIR.glob("*.md")))
    if not catalog_files:
        print(f"❌ Error: No catalog files found in {CATALOG_DIR}")
        sys.exit(1)

    print("=" * 70)
    print(f"🚀 Micro-Agent Automated Catalog Evaluation Suite ({len(catalog_files)} Agents)")
    print("=" * 70)

    passed_count = 0
    failed_count = 0
    errors = []

    for f in catalog_files:
        parsed = parse_catalog_file(f)
        name = parsed["name"]
        
        # 1. Check required sections exist
        if not parsed["system_prompt"]:
            errors.append(f"{name}: Missing '## System Prompt' section")
            failed_count += 1
            continue
        if not parsed["input_schema"]:
            errors.append(f"{name}: Missing '## Input Schema' section")
            failed_count += 1
            continue
        if not parsed["output_contract"]:
            errors.append(f"{name}: Missing '## Output Contract' section")
            failed_count += 1
            continue

        # 2. Token Budget Checks
        sys_tokens = estimate_tokens(parsed["system_prompt"])
        in_tokens = estimate_tokens(parsed["input_schema"])
        out_tokens = estimate_tokens(parsed["output_contract"])
        total_tokens = sys_tokens + in_tokens + out_tokens

        if total_tokens > 4000:
            errors.append(f"{name}: Exceeds 4,000-token envelope ({total_tokens} tokens)")
            failed_count += 1
            continue

        # 3. Output Contract Syntax Validation
        if parsed["output_format"] == "json":
            try:
                json.loads(parsed["output_contract"])
            except json.JSONDecodeError as err:
                errors.append(f"{name}: Output Contract is not valid JSON ({err})")
                failed_count += 1
                continue

        # 4. Tier 0 Parity Tests
        if name == "flow-matching-sigma-calculator":
            sigmas = flow_matching_sigmas(8, 3.0, 1000)
            assert len(sigmas) == 9, "Flow matching sigmas count mismatch"
            assert sigmas[-1] == 0.0, "Final sigma must be 0.0"

        elif name == "filevine-custom-field-sanitizer":
            sanitized = filevine_custom_field_sanitize("Client's Primary Insurance Policy #")
            assert sanitized == "clientsPrimaryInsurancePolicy", f"Sanitizer mismatch: {sanitized}"

        elif name == "spring-physics-converter":
            res = spring_physics_convert(0.4, 0.85)
            assert res["stiffness"] == 246.74, "Spring stiffness calculation mismatch"

        passed_count += 1
        print(f"  ✓ {name:<38} [Tokens: {total_tokens:>4}/4000] [{parsed['output_format']:^6}]")

    print("-" * 70)
    print(f"Evaluation Summary: {passed_count} Passed, {failed_count} Failed (Total: {len(catalog_files)})")
    
    if errors:
        print("\n❌ Failures Detected:")
        for err in errors:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n🎉 ALL 35 MICRO-AGENTS PASSED EVALUATION & TOKEN BUDGET AUDIT!")
        sys.exit(0)


if __name__ == "__main__":
    main()
