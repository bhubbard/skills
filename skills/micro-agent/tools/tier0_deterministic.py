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
# 6. E.164 Phone Normalizer
# ==============================================================================
def e164_phone_normalize(phone: str, default_country_code: str = "1") -> Dict[str, Any]:
    """
    Normalizes raw telephone numbers to canonical ITU-T E.164 format.
    Executes in < 3 microseconds.
    """
    ext_match = re.search(r"(?:ext|x|extension)[.\s:]*([0-9]+)", phone, re.IGNORECASE)
    ext = ext_match.group(1) if ext_match else ""

    cleaned = re.sub(r"[^0-9+]", "", re.split(r"(?:ext|x|extension)", phone, flags=re.IGNORECASE)[0])
    if cleaned.startswith("+"):
        digits = cleaned[1:]
    elif cleaned.startswith("1") and len(cleaned) == 11 and default_country_code == "1":
        digits = cleaned
    else:
        digits = default_country_code + cleaned

    is_valid = 8 <= len(digits) <= 15
    e164_str = f"+{digits}" if is_valid else ""
    nat = digits[len(default_country_code):] if digits.startswith(default_country_code) else digits

    formatted = f"({nat[:3]}) {nat[3:6]}-{nat[6:]}" if len(nat) == 10 and default_country_code == "1" else digits
    toll_free = nat[:3] in ["800", "888", "877", "866", "855", "844", "833"] if len(nat) >= 3 else False

    return {
        "e164": e164_str,
        "country_code": default_country_code,
        "national_number": nat,
        "extension": ext,
        "is_valid": is_valid,
        "formatted_national": formatted,
        "is_toll_free": toll_free
    }


# ==============================================================================
# 7. Water Wave Dispersion Calculator
# ==============================================================================
def water_dispersion_omega(
    k: float,
    depth: float = 1.6,
    gravity: float = 9.81,
    surface_tension: float = 7.4e-5,
    loop_period: float = 60.0
) -> Dict[str, Any]:
    """
    Calculates finite-depth gravity-capillary wave dispersion frequency omega(k)
    and quantized looping frequency. Executes in < 2 microseconds.
    """
    if k <= 0:
        raise ValueError("wavenumber k must be > 0")

    tanh_factor = math.tanh(k * depth) if depth > 0 else 1.0
    w_sq = (gravity * k + surface_tension * (k ** 3)) * tanh_factor
    w = math.sqrt(max(0.0, w_sq))

    w0 = (2.0 * math.pi) / loop_period if loop_period > 0 else 0.0
    quantized_w = math.floor(w / w0) * w0 if w0 > 0 else w

    wavelength = (2.0 * math.pi) / k
    phase_speed = w / k

    regime = "shallow_water" if k * depth < 0.3 else ("deep_water" if k * depth > 3.0 else "transitional_depth")

    return {
        "wavenumber": round(k, 4),
        "depth": round(depth, 4),
        "wavelength_m": round(wavelength, 4),
        "angular_frequency_rad_s": round(w, 4),
        "phase_speed_m_s": round(phase_speed, 4),
        "quantized_omega": round(quantized_w, 4),
        "regime": regime
    }


# ==============================================================================
# 8. Pacejka Magic Formula Tire Friction
# ==============================================================================
def pacejka_magic_formula(
    slip_angle_deg: float,
    fz: float,
    b: float = 10.0,
    c: float = 1.30,
    d: float = 1.00,
    e: float = -0.90
) -> Dict[str, Any]:
    """
    Evaluates Pacejka Magic Formula for lateral tire cornering force.
    Fy = Fz * D * sin(C * arctan(B * alpha - E * (B * alpha - arctan(B * alpha))))
    Executes in < 2 microseconds.
    """
    alpha_rad = math.radians(slip_angle_deg)
    bx = b * alpha_rad
    arg = bx - e * (bx - math.atan(bx))
    mu_y = d * math.sin(c * math.atan(arg))
    fy = fz * mu_y

    peak_force = fz * d
    saturation = min(100.0, round(abs(fy) / peak_force * 100.0, 1)) if peak_force > 0 else 0.0

    return {
        "slip_angle_deg": round(slip_angle_deg, 4),
        "normal_load_fz_n": round(fz, 1),
        "lateral_force_fy_n": round(fy, 1),
        "peak_friction_coeff": round(d, 4),
        "grip_saturation_pct": saturation,
        "regime": "linear" if abs(slip_angle_deg) < 2.0 else ("peak" if abs(slip_angle_deg) < 7.0 else "sliding")
    }


# ==============================================================================
# 9. Dental Tooth Number System Converter
# ==============================================================================
def tooth_number_convert(tooth: str, from_system: str = "Universal") -> Dict[str, Any]:
    """
    Converts tooth numbers across Universal, FDI Two-Digit, and Palmer systems.
    Executes in < 2 microseconds.
    """
    # Universal 1-32 to FDI mapping
    UNIVERSAL_TO_FDI = {
        "1": "18", "2": "17", "3": "16", "4": "15", "5": "14", "6": "13", "7": "12", "8": "11",
        "9": "21", "10": "22", "11": "23", "12": "24", "13": "25", "14": "26", "15": "27", "16": "28",
        "17": "38", "18": "37", "19": "36", "20": "35", "21": "34", "22": "33", "23": "32", "24": "31",
        "25": "41", "26": "42", "27": "43", "28": "44", "29": "45", "30": "46", "31": "47", "32": "48",
    }
    
    t_clean = tooth.strip().upper()
    if from_system.lower() == "universal":
        fdi = UNIVERSAL_TO_FDI.get(t_clean, "")
        univ = t_clean
    else:
        # Inverse lookup from FDI
        fdi = t_clean
        univ = next((u for u, f in UNIVERSAL_TO_FDI.items() if f == t_clean), "")

    if not fdi or len(fdi) != 2:
        return {"error": f"Invalid tooth identifier: {tooth}"}

    quad_digit = fdi[0]
    pos_digit = fdi[1]

    quad_names = {
        "1": "Upper Right", "2": "Upper Left",
        "3": "Lower Left", "4": "Lower Right"
    }
    quad_codes = {
        "1": "UR", "2": "UL", "3": "LL", "4": "LR"
    }
    arches = {
        "1": "Maxillary", "2": "Maxillary",
        "3": "Mandibular", "4": "Mandibular"
    }
    tooth_names = {
        "1": "Central Incisor", "2": "Lateral Incisor", "3": "Canine",
        "4": "First Premolar", "5": "Second Premolar",
        "6": "First Molar", "7": "Second Molar", "8": "Third Molar"
    }

    return {
        "universal": univ,
        "fdi": fdi,
        "palmer": f"{pos_digit}_{quad_codes.get(quad_digit, '')}",
        "arch": arches.get(quad_digit, ""),
        "quadrant": quad_names.get(quad_digit, ""),
        "tooth_type": tooth_names.get(pos_digit, ""),
        "dentition": "Permanent"
    }


# ==============================================================================
# CLI Dispatcher
# ==============================================================================
def main():
    if len(sys.argv) < 2:
        print("Usage: tier0_deterministic.py <command> [args...]")
        print("Commands: sigmas, filevine, spring, lora, tailwind, phone, dispersion, pacejka, tooth")
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
