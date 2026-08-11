"""Tests for PPTX color macro no-ops (texmath/OMML compatibility)."""

import os
import re
import shutil
import subprocess

import pytest

import lamd


def _macro_file_path(filename: str = "talk-macros-pptx.gpp") -> str:
    return os.path.join(os.path.dirname(lamd.__file__), "macros", filename)


def _read_macro_file(filename: str = "talk-macros-pptx.gpp") -> str:
    path = _macro_file_path(filename)
    assert os.path.exists(path), f"Macro file not found: {path}"
    with open(path) as f:
        return f.read()


class TestPptxColorMacroNoops:
    """PPTX must strip \\color before pandoc; OMML does not support colored math."""

    COLOR_WRAPPER_MACROS = (
        "colorcyan",
        "colormagenta",
        "coloryellow",
        "colorred",
        "colorgreen",
        "colorblue",
    )

    def test_color_two_arg_macro_is_identity(self) -> None:
        content = _read_macro_file()
        match = re.search(
            r"\\define\{\\color\{col\}\{block\}\}\{(?P<body>[^}]*)\}",
            content,
        )
        assert match is not None, r"\color{col}{block} must be defined in talk-macros-pptx.gpp"
        assert match.group("body").strip() == r"\block", r"\color{col}{block} must pass through its second argument only"

    def test_color_wrapper_macros_are_identity(self) -> None:
        content = _read_macro_file()
        for name in self.COLOR_WRAPPER_MACROS:
            match = re.search(
                rf"\\define{{\\{name}\{{block\}}}}\{{(?P<body>[^}}]*)\}}",
                content,
            )
            assert match is not None, f"\\{name}{{block}} must be defined in talk-macros-pptx.gpp"
            assert match.group("body").strip() == r"\block", f"\\{name}{{block}} must be a no-op (content only) for PPTX"

    @pytest.mark.skipif(shutil.which("gpp") is None, reason="gpp not available")
    def test_gpp_strips_color_from_math_before_pandoc(self) -> None:
        """Integration: gpp with PPTX macros should remove \\color from display math."""
        gpp_input = r"""
\define{\redColor}{red}
\define{\magentaColor}{magenta}
\define{\mappingScalar_0}{w_0}
\define{\mappingScalar_1}{w_1}
\define{\color{col}{block}}{\block}

$$ f(x) = {\color{\redColor}{\mappingScalar_0}} + {\color{\magentaColor}{\mappingScalar_1 x}} $$
"""
        result = subprocess.run(
            ["gpp", "-T"],
            input=gpp_input,
            capture_output=True,
            text=True,
            check=True,
        )
        output = result.stdout
        assert r"\color" not in output, f"Expected \\color stripped, got: {output!r}"
        assert "w_0" in output and "w_1" in output
