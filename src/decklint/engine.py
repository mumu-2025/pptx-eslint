"""Static checks over python-pptx object model."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Pt

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RULES = ROOT / "rules" / "duarte-zen-microsoft.yaml"


def load_rules(path: Path | None, preset: str) -> dict[str, Any]:
    data = yaml.safe_load((path or DEFAULT_RULES).read_text(encoding="utf-8"))
    params: dict[str, Any] = {}
    for rule in data.get("rules", []):
        params[rule["check"]] = dict(rule.get("params") or {})
        params[rule["check"]]["_meta"] = {
            "id": rule["id"],
            "severity": rule["severity"],
            "description": rule["description"],
        }
    # apply preset overrides
    presets = data.get("presets") or {}
    if preset in presets:
        for k, v in (presets[preset].get("overrides") or {}).items():
            if k in params:
                # map override keys onto check param names
                if k == "max_chars_per_slide":
                    params["max_chars_per_slide"]["max"] = v
                elif k == "min_font_pt":
                    params["min_font_pt"]["min"] = v
                elif k == "max_accent_colors":
                    params["max_accent_colors"]["max"] = v
            else:
                # also allow creating soft params
                params.setdefault(k, {})[k.split("_")[-1] if False else "value"] = v
                if k == "max_chars_per_slide":
                    params.setdefault("max_chars_per_slide", {"_meta": params.get("max_chars_per_slide", {}).get("_meta", {"id": "max-text", "severity": "error", "description": k})})
                    params["max_chars_per_slide"]["max"] = v
                if k == "min_font_pt":
                    params.setdefault("min_font_pt", {"_meta": {"id": "min-font", "severity": "error", "description": k}})
                    params["min_font_pt"]["min"] = v
    return {"raw": data, "params": params}


def lint_pptx(
    path: Path,
    preset: str = "stage",
    rules_path: Path | None = None,
    do_fix: bool = False,
) -> dict[str, Any]:
    cfg = load_rules(rules_path, preset)
    prs = Presentation(str(path))
    violations: list[dict[str, Any]] = []

    for i, slide in enumerate(prs.slides, start=1):
        violations.extend(_check_slide(slide, i, cfg["params"]))

    if do_fix:
        # v0 stub: strip known-decorative animation names when present in XML
        _safe_strip_animations(prs)
        out = path.with_name(path.stem + ".linted.pptx")
        prs.save(str(out))

    score = _score(violations)
    return {
        "file": str(path),
        "preset": preset,
        "score": score,
        "violations": violations,
        "fixed_path": str(path.with_name(path.stem + ".linted.pptx")) if do_fix else None,
    }


def _check_slide(slide, idx: int, params: dict) -> list[dict]:
    out: list[dict] = []
    texts: list[str] = []
    fonts: list[float] = []
    bullets = 0
    images = 0
    title_candidates = 0

    for shape in slide.shapes:
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            images += 1
        if not shape.has_text_frame:
            continue
        tf = shape.text_frame
        full = "\n".join(p.text for p in tf.paragraphs).strip()
        if not full:
            continue
        texts.append(full)
        # rough title: large box near top
        try:
            if shape.top is not None and shape.top < Pt(120) and len(full) < 80:
                title_candidates += 1
        except Exception:
            pass
        for p in tf.paragraphs:
            if p.level and p.level > 0 or (p.text and p.text.strip().startswith(("•", "-", "·"))):
                bullets += 1
            for run in p.runs:
                if run.font.size:
                    fonts.append(run.font.size.pt)

    char_count = sum(len(t) for t in texts)
    meta = params.get("max_chars_per_slide", {})
    if char_count > meta.get("max", 120):
        out.append(_v(meta, idx, f"{char_count} chars on slide (max {meta.get('max')}) — likely a slideument"))

    meta = params.get("min_font_pt", {})
    if fonts and min(fonts) < meta.get("min", 18):
        out.append(_v(meta, idx, f"smallest font {min(fonts):.0f}pt < {meta.get('min')}pt"))

    meta = params.get("bullet_wall", {})
    if bullets > meta.get("max_bullets", 6):
        out.append(_v(meta, idx, f"{bullets} bullet-like paragraphs (max {meta.get('max_bullets', 6)})"))

    meta = params.get("image_layout", {})
    if images > meta.get("max_images", 2):
        out.append(_v({**meta, "_meta": meta.get("_meta", {"id": "image-bleed", "severity": "info", "description": ""})}, idx, f"{images} images — prefer one large visual"))

    meta = params.get("title_is_claim", {})
    ban = set(meta.get("ban_phrases") or [])
    for t in texts[:2]:
        if any(b.lower() in t.lower() for b in ban):
            out.append(_v(meta, idx, f"title/label looks vague: «{t[:40]}» — prefer a claim"))

    meta = params.get("max_title_boxes", {})
    # soft: many near-top text boxes
    if title_candidates > meta.get("max", 1) + 2:
        out.append(_v(meta, idx, f"{title_candidates} top text frames — possible multi-idea slide"))

    # charts
    for shape in slide.shapes:
        if shape.has_chart:
            meta = params.get("chart_junk", {})
            try:
                chart = shape.chart
                # 3D chart types are harder to detect uniformly; flag missing has_data_labels as soft
                if meta.get("require_data_labels_or_callouts"):
                    # heuristic only
                    out.append(
                        {
                            "severity": "info",
                            "rule": "no-default-chart",
                            "slide": idx,
                            "message": "chart present — manually ensure no 3D/default grid; add callouts (Duarte)",
                        }
                    )
            except Exception:
                pass

    return out


def _v(meta: dict, slide: int, message: str) -> dict:
    m = meta.get("_meta") or {"id": "unknown", "severity": "warning", "description": ""}
    return {"severity": m.get("severity", "warning"), "rule": m.get("id", "unknown"), "slide": slide, "message": message}


def _score(violations: list[dict]) -> int:
    score = 100
    for v in violations:
        score -= {"error": 12, "warning": 5, "info": 1}.get(v["severity"], 3)
    return max(0, score)


def _safe_strip_animations(prs: Presentation) -> None:
    """Best-effort: remove timing nodes that look decorative. v0 no-op if structure unknown."""
    # Kept as extension point; full OOXML timing edit lands in v0.2
    return
