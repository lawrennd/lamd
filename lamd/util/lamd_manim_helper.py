"""lamd_manim_helper — text-conversion helpers for LaMD-generated Manim files.

This module is the *source* file; ``mdpp.py`` copies it alongside every
generated ``.slides.manim.py`` / ``.video.manim.py`` as ``_lamd_manim.py``
so that the generated file can do::

    from _lamd_manim import lamd_text, lamd_display_math

The helpers parse lightweight Markdown (bold, italic, inline math, display
math) and return Manim ``VGroup`` / ``MathTex`` / ``MarkupText`` objects so
that generated Manim code stays clean and readable.

Design constraints
------------------
* Must not import anything at module level that is unavailable in the test
  environment (Manim is NOT installed in CI).  All Manim imports are guarded
  inside each function body.
* The public API is intentionally minimal for Phase 1; richer Markdown
  support (links, code spans, headings) is deferred to Phase 2.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from manim import MarkupText, MathTex, VGroup  # type: ignore[import]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

# Regex that splits on $$...$$ display-math delimiters (multiline).
# Must be applied BEFORE inline-math splitting to avoid mis-parsing.
_DISPLAY_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)

# Regex that splits a string on $...$ inline math delimiters.
# Group 1 captures the LaTeX content between the dollar signs.
# Applied only to plain-text segments (after display math is extracted).
_INLINE_MATH_RE = re.compile(r"\$([^$]+)\$")

# Minimal Markdown → Pango markup conversions (used in MarkupText).
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_ITALIC_RE = re.compile(r"\*(.+?)\*")

# Markdown bullet-list prefix pattern — stripped from plain-text segments.
_BULLET_RE = re.compile(r"^\s*\*\s+", re.MULTILINE)


def _md_to_pango(text: str) -> str:
    """Convert a small subset of Markdown to Pango markup.

    Supported:
    * ``**bold**`` → ``<b>bold</b>``
    * ``*italic*`` → ``<i>italic</i>``

    Everything else is returned verbatim (Pango ignores unknown tags).
    """
    text = _BOLD_RE.sub(r"<b>\1</b>", text)
    text = _ITALIC_RE.sub(r"<i>\1</i>", text)
    return text


def _process_inline_segment(
    text: str,
    font_size: int,
    kwargs: dict,
) -> list:
    """Split a plain-text segment on ``$...$`` and return a list of mobjects.

    Each plain-text sub-segment becomes a ``MarkupText``; each math
    sub-segment becomes a ``MathTex``.  Whitespace-only segments are skipped.
    """
    from manim import MarkupText, MathTex  # type: ignore[import]

    mobjects = []
    parts = _INLINE_MATH_RE.split(text)
    for i, part in enumerate(parts):
        if not part or not part.strip():
            continue
        if i % 2 == 0:
            pango = _md_to_pango(part)
            if pango.strip():
                mobjects.append(MarkupText(pango, font_size=font_size, **kwargs))
        else:
            mobjects.append(MathTex(part.strip(), font_size=font_size, **kwargs))
    return mobjects


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def lamd_text(
    md_string: str,
    font_size: int = 36,
    display_font_size: int = 48,
    **kwargs,
) -> "VGroup | MathTex | MarkupText":
    """Convert a Markdown string into a Manim mobject.

    The string is first split on ``$$...$$`` display-math blocks, then each
    plain-text segment is split on ``$...$`` inline-math delimiters.

    * Display-math blocks → ``MathTex`` at *display_font_size*.
    * Inline-math spans → ``MathTex`` at *font_size*.
    * Plain text → ``MarkupText`` (bold/italic via Pango markup).

    Multiple segments are stacked vertically in a ``VGroup`` when the content
    contains display-math blocks; otherwise arranged horizontally.

    If there is exactly one non-empty segment, it is returned unwrapped.

    Parameters
    ----------
    md_string:
        The Markdown / LaTeX source string (may contain ``$$...$$`` and
        ``$...$``).
    font_size:
        Font size for plain text and inline math.
    display_font_size:
        Font size for display-math blocks (``$$...$$``).
    **kwargs:
        Additional keyword arguments forwarded to each mobject constructor.

    Returns
    -------
    VGroup | MathTex | MarkupText
        A Manim mobject ready to be added to a scene.
    """
    from manim import DOWN, LEFT, MarkupText, MathTex, VGroup  # type: ignore[import]

    if not md_string:
        return MarkupText("", font_size=font_size, **kwargs)

    # --- Step 1: split on $$...$$ display math ---
    display_parts = _DISPLAY_MATH_RE.split(md_string)
    # display_parts = [text, display_math, text, display_math, ..., text]
    # Odd-indexed elements are captured display-math groups.

    has_display = len(display_parts) > 1
    mobjects = []

    for i, seg in enumerate(display_parts):
        if i % 2 == 1:
            # Display-math block
            latex = seg.strip()
            if latex:
                mobjects.append(MathTex(latex, font_size=display_font_size, **kwargs))
        else:
            # Plain / inline-math segment
            mobjects.extend(_process_inline_segment(seg, font_size, kwargs))

    if len(mobjects) == 0:
        return MarkupText("", font_size=font_size, **kwargs)
    if len(mobjects) == 1:
        return mobjects[0]

    group = VGroup(*mobjects)
    if has_display:
        group.arrange(direction=DOWN, aligned_edge=LEFT)
    else:
        group.arrange()
    return group


def lamd_display_math(
    latex_string: str,
    font_size: int = 48,
    **kwargs,
) -> "MathTex":
    """Return a centred ``MathTex`` for a display-mode equation.

    Parameters
    ----------
    latex_string:
        The LaTeX source (without surrounding ``$$`` delimiters).
    font_size:
        Font size for the ``MathTex``.
    **kwargs:
        Additional keyword arguments forwarded to ``MathTex``.

    Returns
    -------
    MathTex
    """
    from manim import MathTex  # type: ignore[import]

    return MathTex(latex_string, font_size=font_size, **kwargs)
