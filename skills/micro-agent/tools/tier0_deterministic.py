#!/usr/bin/env python3
"""
Tier 0 Deterministic Engine for Micro-Agents.
Executes pure-code, zero-token, mathematically exact operations in microseconds.
Bans LLMs from performing deterministic arithmetic, regex sanitation, and physics conversions.
"""

import math
import re
import sys
import json
from typing import List, Dict, Any, Tuple


# ==============================================================================
# 1. Flow Matching Sigma Schedule Calculator
# ==============================================================================
def flow_matching_sigmas(steps: int, shift: float = 1.0, num_train_timesteps: int = 1000) -> List[float]:
    """
    Computes shifted discrete sigma sequences from t=1.0 down to t=0.0.
    Formula: sigma_t = (shift * t) / (1 + (shift - 1) * t)
    Executes in < 2 microseconds.
    """
    if steps <= 0:
        raise ValueError("steps must be > 0")
    if shift <= 0:
        raise ValueError("shift must be > 0")

    sigmas = []
    for i in range(steps):
        t = 1.0 - (i / steps) * (1.0 - 1.0 / num_train_timesteps)
        sigma = (shift * t) / (1.0 + (shift - 1.0) * t)
        sigmas.append(round(sigma, 4))
    sigmas.append(0.0)
    return sigmas


# ==============================================================================
# 2. Filevine Custom Field Sanitizer
# ==============================================================================
def filevine_custom_field_sanitize(label: str) -> str:
    """
    Converts human-readable field labels into valid camelCase Filevine field codes:
    1. Strip non-alphanumeric characters.
    2. Convert words to camelCase.
    3. Truncate to maximum 40 characters.
    Executes in < 5 microseconds.
    """
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", label).strip()
    words = cleaned.split()
    if not words:
        return ""
    
    first = words[0].lower()
    rest = [w.capitalize() for w in words[1:]]
    camel = first + "".join(rest)
    return camel[:40]


# ==============================================================================
# 3. Spring Physics Converter (Apple Fluid Interfaces)
# ==============================================================================
def spring_physics_convert(response: float, damping_ratio: float, mass: float = 1.0) -> Dict[str, Any]:
    """
    Converts designer parameters (response / T_d, damping_ratio / zeta) to physical spring
    constants (stiffness k, damping c, mass m) and CSS timing approximations.
    Formula: omega_n = 2*pi / response, k = mass * omega_n^2, c = 2 * mass * omega_n * damping_ratio
    Executes in < 1 microsecond.
    """
    if response <= 0:
        raise ValueError("response must be > 0")
    if damping_ratio < 0:
        raise ValueError("damping_ratio must be >= 0")

    omega_n = (2.0 * math.pi) / response
    stiffness = round(mass * (omega_n ** 2), 2)
    damping = round(2.0 * mass * omega_n * damping_ratio, 2)
    duration_ms = int(response * 1000)

    return {
        "response": round(response, 4),
        "damping_ratio": round(damping_ratio, 4),
        "stiffness": stiffness,
        "damping": damping,
        "mass": mass,
        "motion_config": {
            "type": "spring",
            "stiffness": stiffness,
            "damping": damping,
            "mass": mass
        },
        "css_transition": f"transform {duration_ms}ms cubic-bezier(0.16, 1, 0.3, 1)"
    }


# ==============================================================================
# 4. LoRA Delta & Scaling Multiplier
# ==============================================================================
def lora_delta_scale(rank: int, alpha: float | None = None) -> float:
    """
    Calculates the exact scaling multiplier scale = alpha / rank.
    """
    if rank <= 0:
        raise ValueError("rank must be > 0")
    a = float(alpha) if alpha is not None else float(rank)
    return round(a / rank, 4)


# ==============================================================================
# 5. Tailwind CSS Class Sorter (Box-Model Cascade Specificity)
# ==============================================================================
TAILWIND_ORDER = [
    # Layout / Display
    r"^(block|inline-block|inline|flex|inline-flex|grid|inline-grid|hidden|table)$",
    r"^(relative|absolute|fixed|sticky|static)$",
    r"^(top|bottom|left|right|inset)-",
    r"^z-",
    # Flex / Grid
    r"^flex-",
    r"^grid-",
    r"^items-",
    r"^justify-",
    r"^gap-",
    # Box Sizing
    r"^w-",
    r"^min-w-",
    r"^max-w-",
    r"^h-",
    r"^min-h-",
    r"^max-h-",
    # Spacing
    r"^m[trblxy]?-",
    r"^p[trblxy]?-",
    # Typography
    r"^font-",
    r"^text-",
    r"^leading-",
    r"^tracking-",
    # Background & Borders
    r"^bg-",
    r"^border",
    r"^rounded",
    r"^shadow",
    # Interactivity / States
    r"^cursor-",
    r"^hover:",
    r"^focus:",
    r"^active:",
    r"^transition",
    r"^transform",
]

def tailwind_class_sort(class_string: str) -> str:
    """
    Sorts Tailwind CSS classes logically according to the CSS box-model cascade.
    """
    classes = class_string.strip().split()
    
    def get_rank(cls: str) -> int:
        for idx, pattern in enumerate(TAILWIND_ORDER):
            if re.search(pattern, cls):
                return idx
        return len(TAILWIND_ORDER)

    sorted_classes = sorted(classes, key=get_rank)
    return " ".join(sorted_classes)


# ==============================================================================
# CLI Dispatcher
# ==============================================================================
def main():
    if len(sys.argv) < 2:
        print("Usage: tier0_deterministic.py <command> [args...]")
        print("Commands: sigmas, filevine, spring, lora, tailwind")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "sigmas":
        # args: steps [shift] [timesteps]
        steps = int(sys.argv[2])
        shift = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        tt = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
        res = flow_matching_sigmas(steps, shift, tt)
        print(json.dumps(res))

    elif cmd == "filevine":
        # args: "Human Label"
        label = " ".join(sys.argv[2:])
        print(filevine_custom_field_sanitize(label))

    elif cmd == "spring":
        # args: response damping_ratio [mass]
        resp = float(sys.argv[2])
        zeta = float(sys.argv[3])
        m = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        res = spring_physics_convert(resp, zeta, m)
        print(json.dumps(res, indent=2))

    elif cmd == "lora":
        # args: rank [alpha]
        rank = int(sys.argv[2])
        alpha = float(sys.argv[3]) if len(sys.argv) > 3 else None
        print(lora_delta_scale(rank, alpha))

    elif cmd == "tailwind":
        # args: "class string"
        cls_str = " ".join(sys.argv[2:])
        print(tailwind_class_sort(cls_str))

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
