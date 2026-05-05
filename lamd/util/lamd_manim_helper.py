"""lamd_manim_helper — text-conversion helpers for LaMD-generated Manim files.

This module is the *source* file; ``mdpp.py`` copies it alongside every
generated ``.slides.manim.py`` / ``.video.manim.py`` as ``_lamd_manim.py``
so that the generated file can do::

    from _lamd_manim import lamd_text, lamd_display_math

The helpers parse lightweight Markdown (bold, italic, inline math) and return
Manim ``VGroup`` / ``MathTex`` / ``MarkupText`` objects so that generated
Manim code stays clean and readable.

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
    from manim import MathTex, MarkupText, VGroup  # type: ignore[import]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

# Regex that splits a string on $...$ inline math delimiters.
# Group 1 captures the LaTeX content between the dollar signs.
_INLINE_MATH_RE = re.compile(r"\$([^$]+)\$")

# Minimal Markdown → Pango markup conversions (used in MarkupText).
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_ITALIC_RE = re.compile(r"\*(.+?)\*")


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


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def lamd_text(
    md_string: str,
    font_size: int = 36,
    **kwargs,
) -> "VGroup | MathTex | MarkupText":
    """Convert a Markdown string into a Manim mobject.

    The string is split on ``$...$`` inline-math delimiters.  Each plain-text
    segment becomes a ``MarkupText`` (with Pango markup from
    :func:`_md_to_pango`) and each math segment becomes a ``MathTex``.
    Multiple segments are arranged left-to-right in a ``VGroup``.

    If there is exactly one segment and it is plain text, a single
    ``MarkupText`` is returned (no ``VGroup`` wrapper).  Likewise, a single
    math-only string returns a bare ``MathTex``.

    Parameters
    ----------
    md_string:
        The Markdown / LaTeX source string.
    font_size:
        Font size passed to ``MarkupText`` / ``MathTex``.
    **kwargs:
        Additional keyword arguments forwarded to each ``MarkupText`` /
        ``MathTex`` constructor.

    Returns
    -------
    VGroup | MathTex | MarkupText
        A Manim mobject ready to be added to a scene.
    """
    from manim import MathTex, MarkupText, VGroup  # type: ignore[import]

    if not md_string:
        return MarkupText("", font_size=font_size, **kwargs)

    parts = _INLINE_MATH_RE.split(md_string)
    # _INLINE_MATH_RE.split returns: [text, math, text, math, ..., text]
    # Odd-indexed elements are captured math groups; even-indexed are plain text.
    mobjects = []
    for i, part in enumerate(parts):
        if not part:
            continue
        if i % 2 == 0:
            # Plain text segment
            pango = _md_to_pango(part)
            mobjects.append(MarkupText(pango, font_size=font_size, **kwargs))
        else:
            # Math segment (captured group between $...$)
            mobjects.append(MathTex(part, font_size=font_size, **kwargs))

    if len(mobjects) == 0:
        return MarkupText("", font_size=font_size, **kwargs)
    if len(mobjects) == 1:
        return mobjects[0]

    group = VGroup(*mobjects)
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
