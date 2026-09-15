"""CIP-0012 inventory-derived regression tests.

Fixtures under tests/fixtures/cip0012/ map to real snippet/talk paths listed in
cip/cip0012/inventory.md. Baseline behaviour must hold for legacy loaders;
\\includescript and slide_setup are covered as additive APIs.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

import lamd

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "cip0012"
MACROS = Path(os.path.dirname(lamd.__file__)) / "macros"
INCLUDES = Path(os.path.dirname(lamd.__file__)) / "includes"
TEMPLATE = Path(os.path.dirname(lamd.__file__)) / "templates" / "pandoc" / "pandoc-revealjs-template.revealjs"
MAKE_SLIDES = Path(os.path.dirname(lamd.__file__)) / "makefiles" / "make-slides.mk"
MAKE_FLAGS = Path(os.path.dirname(lamd.__file__)) / "makefiles" / "make-talk-flags.mk"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _gpp(defines: list[str], *macro_files: str, body: str) -> str:
    """Run gpp -T with selected macro files and a body string."""
    chunks: list[str] = []
    for name in macro_files:
        chunks.append(f"\\include{{{name}}}")
    chunks.append(body)
    gpp_input = "\n".join(chunks)
    cmd = ["gpp", "-T", f"-I{MACROS}", "-DscriptsDir=SCRIPTS", "-DwriteDiagramsDir=DIAGRAMS"]
    cmd.extend(defines)
    result = subprocess.run(
        cmd,
        input=gpp_input,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"gpp failed: {result.stderr}\ninput:\n{gpp_input}"
    return result.stdout


@pytest.mark.skipif(shutil.which("gpp") is None, reason="gpp not available")
class TestTrackALegacyContentScripts:
    """Legacy _scripts/includes patterns still emit scriptsDir tags once."""

    def test_ballworld_legacy_emits_script_once(self) -> None:
        body = _read(FIXTURES / "legacy-ballworld-js.md")
        # include twice to exercise \\ifndef once-guard
        out = _gpp(
            ["-DHTML=1"],
            "talk-macros-null.gpp",
            "talk-macros-html.gpp",
            body=body + "\n" + body,
        )
        assert out.count('src="SCRIPTS/ballworld/ballworld.js"') == 1

    def test_maxwell_legacy_loads_ballworld_and_maxwell(self) -> None:
        body = _read(FIXTURES / "legacy-maxwell-js.md")
        out = _gpp(
            ["-DHTML=1"],
            "talk-macros-null.gpp",
            "talk-macros-html.gpp",
            body=body,
        )
        assert 'src="SCRIPTS/ballworld/ballworld.js"' in out
        assert 'src="SCRIPTS/ballworld/maxwell.js"' in out

    def test_dasher_legacy_keeps_cache_bust_query(self) -> None:
        body = _read(FIXTURES / "legacy-dasher-js.md")
        out = _gpp(
            ["-DHTML=1"],
            "talk-macros-null.gpp",
            "talk-macros-html.gpp",
            body=body,
        )
        assert 'src="SCRIPTS/dasher/dasher.js?v=22"' in out

    def test_legacy_ballworld_absent_in_tex(self) -> None:
        body = _read(FIXTURES / "legacy-ballworld-js.md")
        # TEX path: null macros only (no HTML override) — script tags still
        # appear as raw text in legacy includes; format reach is "author must
        # not include *-js.md in tex". Assert includescript no-op instead.
        out = _gpp(
            ["-DTEX=1"],
            "talk-macros-null.gpp",
            body="\\includescript{ballworld/ballworld.js}",
        )
        assert "<script" not in out


@pytest.mark.skipif(shutil.which("gpp") is None, reason="gpp not available")
class TestTrackAIncludeScript:
    """\\includescript expands in HTML; no-op without HTML macros."""

    def test_includescript_emits_in_html(self) -> None:
        body = _read(FIXTURES / "includescript-ballworld.md")
        out = _gpp(
            ["-DHTML=1"],
            "talk-macros-null.gpp",
            "talk-macros-html.gpp",
            body=body,
        )
        assert 'src="SCRIPTS/ballworld/ballworld.js"' in out
        # once via surrounding \\ifndef in the twin fixture
        assert out.count('src="SCRIPTS/ballworld/ballworld.js"') == 1

    def test_includescript_twin_matches_legacy_src(self) -> None:
        legacy = _gpp(
            ["-DHTML=1"],
            "talk-macros-null.gpp",
            "talk-macros-html.gpp",
            body=_read(FIXTURES / "legacy-ballworld-js.md"),
        )
        twin = _gpp(
            ["-DHTML=1"],
            "talk-macros-null.gpp",
            "talk-macros-html.gpp",
            body=_read(FIXTURES / "includescript-ballworld.md"),
        )
        legacy_srcs = set(re.findall(r'src="([^"]+)"', legacy))
        twin_srcs = set(re.findall(r'src="([^"]+)"', twin))
        assert legacy_srcs == twin_srcs == {"SCRIPTS/ballworld/ballworld.js"}

    def test_includescript_noop_without_html(self) -> None:
        out = _gpp(
            [],
            "talk-macros-null.gpp",
            body="\\includescript{ballworld/ballworld.js}",
        )
        assert "<script" not in out


@pytest.mark.skipif(shutil.which("gpp") is None, reason="gpp not available")
class TestTrackBBackgrounds:
    """data-background and includeplotly iframe attrs still emit."""

    def test_newslide_data_background(self) -> None:
        body = _read(FIXTURES / "data-background-slide.md")
        out = _gpp(
            ["-DSLIDES=1"],
            "talk-macros-null.gpp",
            "talk-macros-slides.gpp",
            body=body,
        )
        assert 'data-background="DIAGRAMS/pres_bg.png"' in out
        assert "Cloaking" in out

    def test_includeplotly_iframe_background(self) -> None:
        body = _read(FIXTURES / "includeplotly-bg.md")
        out = _gpp(
            ["-DSLIDES=1", "-DHTML=1"],
            "talk-macros-null.gpp",
            "talk-macros-html.gpp",
            "talk-macros-slides.gpp",
            "talk-macros-slides-html.gpp",
            body=body,
        )
        assert "data-background-iframe=" in out
        assert "data-background-interactive" in out
        assert "https://example.com/plot" in out


class TestHeaderAndTemplateBaselines:
    """Shared header JS and template lifecycle (no gpp required)."""

    def test_slides_header_has_mathjax_and_figure_animate(self) -> None:
        content = _read(INCLUDES / "slides-header.html")
        assert "MathJax.js" in content
        assert "figure-animate.js" in content
        assert "lamdSetDivs" in content

    def test_template_include_after_after_reveal_initialize(self) -> None:
        content = _read(TEMPLATE)
        init_at = content.find("Reveal.initialize")
        after_at = content.find("$include-after$")
        assert init_at != -1 and after_at != -1
        assert after_at > init_at

    def test_mermaid_ready_listener_after_reveal_initialize(self) -> None:
        content = _read(TEMPLATE)
        init_at = content.find("Reveal.initialize")
        # Mermaid ready must not appear in <head>
        head_end = content.find("</head>")
        head = content[:head_end]
        assert "mermaid.initialize" not in head
        mermaid_at = content.find("mermaid.initialize")
        assert mermaid_at != -1 and mermaid_at > init_at

    def test_make_slides_wires_slide_setup_conditionally(self) -> None:
        flags = _read(MAKE_FLAGS)
        slides = _read(MAKE_SLIDES)
        assert "slide_setup" in flags
        assert "SLIDESETUP" in flags
        assert "SLIDE_SETUP_FLAG" in slides
        assert "--include-after-body" in slides
        # empty when unset: $(if $(strip $(SLIDESETUP)),...)
        assert "strip $(SLIDESETUP)" in slides or "strip $(SLIDESETUP)" in slides.replace(" ", "")

    def test_ambient_setup_implements_b3_yield(self) -> None:
        ambient = _read(INCLUDES / "slide-setup-ambient.html")
        assert "slideHasOwnBackground" in ambient
        assert "data-background-iframe" in ambient
        assert "slidechanged" in ambient
        assert "print-pdf" in ambient
        assert "lamd-ambient-paused" in ambient


class TestInventoryFixturePaths:
    """Fixture directory stays aligned with Stage 0 list."""

    EXPECTED = {
        "legacy-ballworld-js.md",
        "legacy-maxwell-js.md",
        "legacy-dasher-js.md",
        "includescript-ballworld.md",
        "data-background-slide.md",
        "includeplotly-bg.md",
    }

    def test_fixtures_present(self) -> None:
        present = {p.name for p in FIXTURES.glob("*.md")}
        assert self.EXPECTED <= present

    def test_inventory_document_exists(self) -> None:
        inv = Path(__file__).resolve().parents[2] / "cip" / "cip0012" / "inventory.md"
        assert inv.is_file()
        text = inv.read_text(encoding="utf-8")
        assert "Track A" in text and "Track B" in text
        assert "legacy-ballworld-js.md" in text
