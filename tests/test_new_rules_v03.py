"""Unit / integration tests for v0.3 rules and presets."""
from pathlib import Path

import pytest

from decklint.engine import lint_pptx, load_rules
from decklint.rules import CHECKERS, DECK_CHECKERS, list_rules

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "fixtures"


@pytest.fixture(scope="module", autouse=True)
def ensure_fixtures():
    from scripts.make_fixtures import async_no_notes, bad, contrast_fail, duplicate_titles, good

    bad()
    good()
    contrast_fail()
    duplicate_titles()
    async_no_notes()


def test_new_checkers_registered():
    for key in (
        "unique_titles",
        "safe_margins",
        "bullet_depth",
        "speaker_notes",
        "notes_for_charts",
        "vague_links",
        "deck_properties",
        "auto_advance",
        "empty_slide",
        "max_shapes",
        "font_embed",
        "title_length",
    ):
        assert key in CHECKERS
    for key in ("unique_titles", "deck_properties", "auto_advance", "font_embed"):
        assert key in DECK_CHECKERS


def test_list_rules_bilingual_has_v03():
    en = {r["id"] for r in list_rules("en")}
    zh = {r["id"] for r in list_rules("zh")}
    for rid in (
        "unique-titles",
        "safe-margins",
        "bullet-depth",
        "speaker-notes",
        "vague-links",
        "deck-properties",
        "auto-advance",
        "empty-slide",
        "max-shapes",
        "font-embed",
        "title-length",
        "notes-for-charts",
    ):
        assert rid in en
        assert rid in zh
    # zh descriptions present
    for r in list_rules("zh"):
        assert r["description"].strip()


def test_presets_load():
    for preset in ("stage", "reading", "keynote", "a11y", "corporate", "wcag-strict", "async-doc"):
        cfg = load_rules(None, preset)
        assert cfg["preset"] == preset
        assert "max_chars_per_slide" in cfg["params"] or "text_bg_contrast" in cfg["params"]


def test_unique_titles_dup_fixture():
    result = lint_pptx(FIX / "dup-titles" / "dup.pptx", preset="wcag-strict")
    ids = {v.rule_id for v in result.violations}
    assert "unique-titles" in ids
    # wcag-strict bumps to error
    assert any(v.rule_id == "unique-titles" and v.severity == "error" for v in result.violations)


def test_bullet_depth_on_bad():
    result = lint_pptx(FIX / "bad" / "slideument.pptx", preset="stage")
    ids = {v.rule_id for v in result.violations}
    assert "bullet-depth" in ids


def test_async_doc_requires_notes():
    result = lint_pptx(FIX / "async-no-notes" / "no-notes.pptx", preset="async-doc")
    ids = {v.rule_id for v in result.violations}
    assert "speaker-notes" in ids


def test_corporate_preset_loads_font_embed():
    cfg = load_rules(None, "corporate")
    assert "font_embed" in cfg["params"]
    assert cfg["params"]["font_embed"].get("require_embedded") is True


def test_good_still_passes_stage_errors():
    from decklint.engine import should_fail

    result = lint_pptx(FIX / "good" / "claim-slide.pptx", preset="stage")
    assert not should_fail(result.violations, "error")
    assert result.score >= 75
