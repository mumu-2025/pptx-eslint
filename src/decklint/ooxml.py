"""OOXML helpers: open pptx as zip; parse timing / transition XML."""
from __future__ import annotations

import re
import zipfile
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

# Common PowerPoint animation / transition filter names (subset).
BANNED_NAME_HINTS = (
    "bounce",
    "spiral",
    "growturn",
    "swish",
    "whip",
    "boomerang",
    "floats",
    "pinwheel",
    "spinner",
    "credits",
    "flip",
    "fold",
)

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def list_slide_parts(pptx_path: Path) -> list[str]:
    with zipfile.ZipFile(pptx_path, "r") as zf:
        return sorted(
            n
            for n in zf.namelist()
            if re.match(r"ppt/slides/slide\d+\.xml$", n)
        )


def read_part(pptx_path: Path, name: str) -> bytes:
    with zipfile.ZipFile(pptx_path, "r") as zf:
        return zf.read(name)


def parse_slide_animations(pptx_path: Path) -> list[dict]:
    """Return per-slide animation / transition metadata from OOXML."""
    results: list[dict] = []
    for part in list_slide_parts(pptx_path):
        slide_num = int(re.search(r"slide(\d+)", part).group(1))  # type: ignore[union-attr]
        xml = read_part(pptx_path, part)
        root = ET.fromstring(xml)
        transitions: list[str] = []
        effects: list[str] = []

        for child in root:
            tag = _local(child.tag)
            if tag == "transition":
                for tchild in list(child):
                    transitions.append(_local(tchild.tag))
            if tag == "timing":
                for el in child.iter():
                    name = el.attrib.get("name") or el.attrib.get("filter") or ""
                    if name:
                        effects.append(name)
                    # preset class often encodes effect family
                    preset = el.attrib.get("presetClass") or ""
                    preset_id = el.attrib.get("presetID") or ""
                    if preset:
                        effects.append(f"{preset}:{preset_id}")

        # also scan raw text for known decorative filter names
        raw = xml.decode("utf-8", errors="ignore").lower()
        for hint in BANNED_NAME_HINTS:
            if hint in raw:
                effects.append(hint)

        results.append(
            {
                "slide": slide_num,
                "part": part,
                "transitions": sorted(set(transitions)),
                "effects": sorted(set(e for e in effects if e)),
            }
        )
    return results


def strip_banned_animations(
    pptx_path: Path,
    out_path: Path,
    ban_effects: Iterable[str] | None = None,
) -> int:
    """
    Copy pptx and remove timing / transition nodes that match banned names.
    Returns number of parts modified.
    """
    ban = {b.lower() for b in (ban_effects or BANNED_NAME_HINTS)}
    modified = 0
    with zipfile.ZipFile(pptx_path, "r") as zin, zipfile.ZipFile(
        out_path, "w", compression=zipfile.ZIP_DEFLATED
    ) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if re.match(r"ppt/slides/slide\d+\.xml$", item.filename):
                new_data, changed = _strip_from_slide_xml(data, ban)
                if changed:
                    modified += 1
                    data = new_data
            zout.writestr(item, data)
    return modified


def _strip_from_slide_xml(data: bytes, ban: set[str]) -> tuple[bytes, bool]:
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return data, False
    changed = False
    # Remove entire <p:timing> if any banned hint appears in its XML subtree
    timing_nodes = [c for c in list(root) if _local(c.tag) == "timing"]
    for node in timing_nodes:
        blob = ET.tostring(node, encoding="unicode").lower()
        if any(b in blob for b in ban):
            root.remove(node)
            changed = True
    # Strip decorative transition children
    for child in list(root):
        if _local(child.tag) == "transition":
            blob = ET.tostring(child, encoding="unicode").lower()
            if any(b in blob for b in ban):
                root.remove(child)
                changed = True
    if not changed:
        return data, False
    # Preserve default namespace prefixes reasonably
    xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    return xml, True


def _local(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[-1]
    return tag
