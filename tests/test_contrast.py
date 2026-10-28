"""Contrast math unit tests."""
from decklint.contrast import (
    contrast_ratio,
    is_large_text,
    is_near_gray,
    passes_aa,
    relative_luminance,
)


def test_black_white_ratio():
    r = contrast_ratio((0, 0, 0), (255, 255, 255))
    assert abs(r - 21.0) < 0.01


def test_same_color_ratio():
    assert abs(contrast_ratio((128, 128, 128), (128, 128, 128)) - 1.0) < 0.01


def test_gray_on_white_fails_aa():
    ratio = contrast_ratio((200, 200, 200), (255, 255, 255))
    assert ratio < 4.5
    assert not passes_aa(ratio, large=False)


def test_white_on_near_black_passes():
    ratio = contrast_ratio((255, 255, 255), (10, 10, 12))
    assert ratio >= 4.5
    assert passes_aa(ratio, large=False)


def test_large_text_threshold():
    assert is_large_text(24, False)
    assert is_large_text(18, True)
    assert not is_large_text(18, False)
    assert not is_large_text(12, True)


def test_luminance_bounds():
    assert relative_luminance((0, 0, 0)) == 0.0
    assert abs(relative_luminance((255, 255, 255)) - 1.0) < 1e-6


def test_near_gray():
    assert is_near_gray((180, 182, 179))
    assert not is_near_gray((220, 40, 40))
