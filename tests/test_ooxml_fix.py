"""OOXML animation parse / strip smoke tests."""
from pathlib import Path

from decklint.ooxml import list_slide_parts, parse_slide_animations, strip_banned_animations

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "fixtures"


def test_list_parts(tmp_path):
    from scripts.make_fixtures import good

    good()
    path = FIX / "good" / "claim-slide.pptx"
    parts = list_slide_parts(path)
    assert parts
    meta = parse_slide_animations(path)
    assert isinstance(meta, list)
    out = tmp_path / "out.pptx"
    # should not throw even with nothing to strip
    strip_banned_animations(path, out)
    assert out.exists()
