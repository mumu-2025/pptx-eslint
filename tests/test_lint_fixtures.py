"""Integration: bad vs good fixtures + contrast-fail."""
from pathlib import Path

import pytest

from decklint.engine import lint_pptx, should_fail

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "fixtures"


@pytest.fixture(scope="module", autouse=True)
def ensure_fixtures():
    from scripts.make_fixtures import bad, contrast_fail, good

    bad()
    good()
    contrast_fail()


def test_bad_fixture_fails():
    result = lint_pptx(FIX / "bad" / "slideument.pptx", preset="stage")
    assert result.violations
    assert should_fail(result.violations, "error")
    ids = {v.rule_id for v in result.violations}
    assert "max-text" in ids or "no-slideument" in ids or "min-font" in ids


def test_good_fixture_clean_or_soft():
    result = lint_pptx(FIX / "good" / "claim-slide.pptx", preset="stage")
    assert not should_fail(result.violations, "error")
    assert result.score >= 80


def test_contrast_fail_fixture():
    result = lint_pptx(FIX / "contrast-fail" / "gray-on-white.pptx", preset="a11y")
    ids = {v.rule_id for v in result.violations}
    assert "text-contrast" in ids


def test_violation_schema():
    result = lint_pptx(FIX / "bad" / "slideument.pptx", preset="stage")
    assert result.violations
    v = result.violations[0]
    d = v.to_dict()
    for key in (
        "rule_id",
        "severity",
        "slide",
        "message_en",
        "message_zh",
        "fix_hint_en",
        "fix_hint_zh",
        "category",
    ):
        assert key in d
    assert d["message_en"]
    assert d["message_zh"]


def test_json_roundtrip_fields():
    result = lint_pptx(FIX / "bad" / "slideument.pptx", preset="stage")
    payload = result.to_dict(lang="zh")
    assert "violations" in payload
    assert payload["violations"][0]["message"]  # localized
    assert "category_scores" in payload


def test_bilingual_messages_present():
    result = lint_pptx(FIX / "bad" / "slideument.pptx", preset="stage")
    for v in result.violations:
        assert v.message_en.strip()
        assert v.message_zh.strip()
