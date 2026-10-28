"""WCAG 2.x relative luminance and contrast ratio for solid RGB."""
from __future__ import annotations


def _channel(c: float) -> float:
    """Linearize an sRGB channel in 0..1."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """WCAG relative luminance for an 8-bit RGB triple."""
    r, g, b = (x / 255.0 for x in rgb)
    R, G, B = _channel(r), _channel(g), _channel(b)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def contrast_ratio(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    """Contrast ratio between two solid RGB colors (WCAG)."""
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def is_large_text(pt: float | None, bold: bool | None) -> bool:
    """WCAG large text: ≥18pt bold or ≥24pt."""
    if pt is None:
        return False
    if bold and pt >= 18:
        return True
    return pt >= 24


def passes_aa(ratio: float, large: bool) -> bool:
    """WCAG AA: 4.5 normal, 3.0 large."""
    return ratio >= (3.0 if large else 4.5)


def is_near_gray(rgb: tuple[int, int, int], max_delta: int = 18) -> bool:
    """True if R≈G≈B (near-gray / neutral)."""
    r, g, b = rgb
    return max(r, g, b) - min(r, g, b) <= max_delta
