#!/usr/bin/env python3
"""
Token Budget Validator for Micro-Agents.
Calculates token length using standard BPE approximation or tiktoken (cl100k_base).
Enforces the 4,000-token hard envelope rule.
"""

import argparse
import sys
from pathlib import Path

def estimate_tokens(text: str) -> int:
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        # High-accuracy fallback heuristic for code & prose
        words = len(text.split())
        chars = len(text)
        # Average between character-based and word-based estimation
        return int((chars / 3.5 + words * 1.3) / 2)

def main():
    parser = argparse.ArgumentParser(description="Validate 4k Token Budget for Micro-Agents")
    parser.add_argument("--system", type=Path, help="System prompt file")
    parser.add_argument("--input", type=Path, help="Sample input payload file")
    parser.add_argument("--output", type=Path, help="Sample output generation file")
    parser.add_argument("--tool", type=Path, help="Tool schema JSON file (optional)")

    args = parser.parse_args()

    sys_text = args.system.read_text(encoding="utf-8") if args.system and args.system.exists() else ""
    in_text = args.input.read_text(encoding="utf-8") if args.input and args.input.exists() else ""
    out_text = args.output.read_text(encoding="utf-8") if args.output and args.output.exists() else ""
    tool_text = args.tool.read_text(encoding="utf-8") if args.tool and args.tool.exists() else ""

    sys_tokens = estimate_tokens(sys_text)
    tool_tokens = estimate_tokens(tool_text)
    in_tokens = estimate_tokens(in_text)
    out_tokens = estimate_tokens(out_text)
    total_tokens = sys_tokens + tool_tokens + in_tokens + out_tokens

    print("📊 Micro-Agent Token Budget Report:")
    print("--------------------------------------------------")
    print(f"  • System Prompt:    {sys_tokens:>5} tokens (Budget: <= 300)")
    print(f"  • Tool Schema:      {tool_tokens:>5} tokens (Budget: <= 300)")
    print(f"  • Input Payload:    {in_tokens:>5} tokens (Budget: <= 2500)")
    print(f"  • Output Reserve:   {out_tokens:>5} tokens (Budget: <= 1000)")
    print("--------------------------------------------------")
    print(f"  Total Allocation:   {total_tokens:>5} / 4000 tokens")

    if total_tokens > 4000:
        print(f"\n❌ VIOLATION: Exceeds 4,000-token envelope by {total_tokens - 4000} tokens!")
        sys.exit(1)
    else:
        headroom = 4000 - total_tokens
        print(f"\n✅ PASSED: Within budget ({headroom} tokens headroom remaining)")
        sys.exit(0)

if __name__ == "__main__":
    main()
