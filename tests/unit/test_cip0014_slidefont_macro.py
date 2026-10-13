"""CIP-0014: \\slidefont helper is defined for Reveal slide attrs."""

import os
import re

import lamd


def _slides_macros() -> str:
    path = os.path.join(os.path.dirname(lamd.__file__), "macros", "talk-macros-slides.gpp")
    with open(path, encoding="utf-8") as f:
        return f.read()


def test_slidefont_macro_defined():
    content = _slides_macros()
    match = re.search(r"\\define\{\\slidefont\{size\}\}\{([^}]*)\}", content)
    assert match is not None, r"\slidefont{size} must be defined in talk-macros-slides.gpp"
    assert match.group(1).strip() == r".font-\size"


def test_newslide_still_accepts_commands_attrs():
    content = _slides_macros()
    assert r"\define{\newslide{text}{commands}}" in content
    assert r"\define{\section{text}{commands}}" in content
