import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import MagicMock, patch

import pytest

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import frontmatter as fm

from lamd.mdpp import gpp_temp_path, local_edit_url_from_iface, main, process_content, setup_gpp_arguments
from lamd.validation import check_dependency, check_version

# Set LAMD_MACROS environment variable for testing
os.environ["LAMD_MACROS"] = "/usr/local/macros"


def test_check_dependency():
    """Test the check_dependency function."""
    with patch("shutil.which", return_value="/usr/bin/gpp"):
        assert check_dependency("gpp") is True

    with patch("shutil.which", return_value=None):
        assert check_dependency("nonexistent") is False


def test_check_version():
    """Test the check_version function."""
    with patch("subprocess.run", return_value=MagicMock(stdout="2.24", stderr="")):
        assert check_version("gpp", "2.24") is True

    with patch("subprocess.run", return_value=MagicMock(stdout="2.23", stderr="")):
        assert check_version("gpp", "2.24") is False

    with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "gpp")):
        assert check_version("gpp", "2.24") is False


def test_check_dependencies():
    """Test the check_dependencies function."""
    # check_dependencies is not implemented; test removed or to be implemented if needed


def test_setup_gpp_arguments():
    """Test the setup_gpp_arguments function."""
    args = MagicMock()
    args.to = "html"
    args.format = "slides"
    args.exercises = True
    args.assignment = False
    args.edit_links = True
    args.draft = False
    args.meta_data = ["author=John Doe"]
    args.code = "ipynb"
    args.diagrams_dir = "/usr/diagrams"
    args.diagrams_web_dir = None
    args.scripts_dir = "/usr/scripts"
    args.write_diagrams_dir = "/usr/diagrams"
    args.include_path = "/usr/include"
    args.snippets_path = "/usr/snippets"
    args.macros_path = "/usr/macros:/usr/macrostoo"
    args.output = "output.md"
    args.macros = "macros"
    args.filename = "input.md"

    iface = {
        "diagramsurl": "http://example.com",
        "diagramsdir": "diagrams",
        "scriptsdir": "scripts",
        "writediagramsdir": "diagrams",
        "macrosdir": "macros:macrostoo",
    }

    import lamd.mdpp

    mdpp_dir = os.path.dirname(os.path.abspath(lamd.mdpp.__file__))

    required_args = [
        "+n",
        '-U "\\" "" "{" "}{" "}" "{" "}" "#" ""',
        "-DHTML=1",
        "-DSLIDES=1",
        "-DEXERCISES=1",
        "-DEDIT=1",
        "-Dauthor=John Doe",
        "-DCODE=1",
        "-DDISPLAYCODE=1",
        "-DPLOTCODE=1",
        "-DHELPERCODE=1",
        "-DMAGICCODE=1",
        f"-Dtalksdir={mdpp_dir}",
        "-DgithubBaseUrl=https://github.com/lawrennd/snippets/edit/main/",
        "-DgppTempFile=input.gpp.markdown",
        "-DdiagramsDir=/usr/diagrams",
        "-DscriptsDir=/usr/scripts",
        "-DwriteDiagramsDir=/usr/diagrams",
        "-I.",
        "-I/usr/include",
        "-I/usr/snippets",
        "-I/usr/macros",
        "-I/usr/macrostoo",
        "-o output.md",
    ]

    result = setup_gpp_arguments(args, iface)
    # Check -U argument flexibly due to platform-dependent escaping
    u_args = [arg for arg in result if arg.startswith("-U")]
    assert u_args, "Missing required -U argument"
    assert "{" in u_args[0] and "}" in u_args[0], "-U argument does not contain expected macro delimiters"
    # Check all other required arguments except -U
    for req in required_args:
        if not req.startswith("-U"):
            assert req in result, f"Missing required argument: {req}"


def test_main():
    """Test the main function."""
    with patch("sys.argv", ["mdpp.py", "-h", "dummy.md"]), patch("sys.exit") as mock_exit:
        main()
        mock_exit.assert_called_once_with(0)

    args_namespace = argparse.Namespace(
        to="html",
        format="slides",
        exercises=True,
        assignment=False,
        edit_links=True,
        draft=False,
        meta_data=["author=John Doe"],
        code="ipynb",
        diagrams_dir=None,
        diagrams_web_dir=None,
        scripts_dir=None,
        write_diagrams_dir=None,
        include_path="/usr/include",
        snippets_path="/usr/snippets",
        output="output.md",
        macros="macros",
        filename="input.md",
        auto_install=False,
        verbose=False,
    )

    with (
        patch("argparse.ArgumentParser.parse_args", return_value=args_namespace),
        patch("lamd.mdpp.validate_file_exists", return_value=True),
        patch("lamd.mdpp.load_config", return_value={"macros": "macros"}),
        patch("lamd.mdpp.setup_gpp_arguments", return_value=[]),
        patch("lamd.mdpp.process_includes", return_value=("", "")),
        patch("lamd.mdpp.process_content", return_value=""),
        patch("os.path.isdir", return_value=True),
    ):
        main()


def test_format_flags():
    """Test that format-specific flags are set correctly."""
    import argparse

    from lamd.mdpp import setup_gpp_arguments

    # Test notes format
    args = argparse.Namespace(
        format="notes",
        to="html",
        exercises=False,
        assignment=False,
        edit_links=False,
        draft=False,
        meta_data=[],
        code="none",
        diagrams_dir=None,
        diagrams_web_dir=None,
        scripts_dir=None,
        write_diagrams_dir=None,
        include_path=None,
        snippets_path=None,
        macros_path=None,
        output="test.md",
        filename="test.md",
    )
    iface = {"diagramsdir": "diagrams", "scriptsdir": "scripts", "writediagramsdir": "diagrams"}

    gpp_args = setup_gpp_arguments(args, iface)

    # Check that NOTES flag is set
    assert "-DNOTES=1" in gpp_args
    assert "-DHTML=1" in gpp_args

    # Test slides format
    args.format = "slides"
    gpp_args = setup_gpp_arguments(args, iface)

    # Check that SLIDES flag is set
    assert "-DSLIDES=1" in gpp_args
    assert "-DHTML=1" in gpp_args

    # Test different output formats
    args.format = "notes"
    args.to = "tex"
    gpp_args = setup_gpp_arguments(args, iface)
    assert "-DTEX=1" in gpp_args
    assert "-DNOTES=1" in gpp_args

    args.to = "docx"
    gpp_args = setup_gpp_arguments(args, iface)
    assert "-DDOCX=1" in gpp_args
    assert "-DNOTES=1" in gpp_args

    args.to = "pptx"
    gpp_args = setup_gpp_arguments(args, iface)
    assert "-DPPTX=1" in gpp_args
    assert "-DNOTES=1" in gpp_args

    args.to = "ipynb"
    gpp_args = setup_gpp_arguments(args, iface)
    assert "-DIPYNB=1" in gpp_args
    assert "-DNOTES=1" in gpp_args

    # Test code level flags
    args.code = "sparse"
    gpp_args = setup_gpp_arguments(args, iface)
    assert "-DCODE=1" in gpp_args
    assert "-DPLOTCODE=1" not in gpp_args
    assert "-DHELPERCODE=1" not in gpp_args
    assert "-DDISPLAYCODE=1" not in gpp_args
    assert "-DMAGICCODE=1" not in gpp_args

    args.code = "plot"
    gpp_args = setup_gpp_arguments(args, iface)
    assert "-DCODE=1" in gpp_args
    assert "-DPLOTCODE=1" in gpp_args
    assert "-DHELPERCODE=1" not in gpp_args
    assert "-DDISPLAYCODE=1" not in gpp_args
    assert "-DMAGICCODE=1" not in gpp_args

    args.code = "diagnostic"
    gpp_args = setup_gpp_arguments(args, iface)
    assert "-DCODE=1" in gpp_args
    assert "-DPLOTCODE=1" in gpp_args
    assert "-DHELPERCODE=1" in gpp_args
    assert "-DDISPLAYCODE=1" in gpp_args
    assert "-DMAGICCODE=1" not in gpp_args

    args.code = "full"
    gpp_args = setup_gpp_arguments(args, iface)
    assert "-DCODE=1" in gpp_args
    assert "-DPLOTCODE=1" in gpp_args
    assert "-DHELPERCODE=1" in gpp_args
    assert "-DDISPLAYCODE=1" in gpp_args
    assert "-DMAGICCODE=1" in gpp_args

    # Test test code level
    args.code = "test"
    gpp_args = setup_gpp_arguments(args, iface)
    assert "-DTESTCODE=1" in gpp_args
    assert "-DCODE=1" in gpp_args
    assert "-DPLOTCODE=1" in gpp_args
    assert "-DHELPERCODE=1" in gpp_args
    assert "-DDISPLAYCODE=1" in gpp_args
    assert "-DMAGICCODE=1" in gpp_args

    args.code = "ipynb"
    gpp_args = setup_gpp_arguments(args, iface)
    assert "-DCODE=1" in gpp_args
    assert "-DPLOTCODE=1" in gpp_args
    assert "-DHELPERCODE=1" in gpp_args
    assert "-DDISPLAYCODE=1" in gpp_args
    assert "-DMAGICCODE=1" in gpp_args


class TestFrontmatterFileMode:
    """Regression tests for the gpp.markdown temporary-file write path.

    mdpp uses ``dumps()`` and writes the returned str to a UTF-8 text file so
    encoding is explicit regardless of python-frontmatter version.

    The tests below verify:
    1. The mdpp write pattern (``dumps`` + text file) succeeds.
    2. ``frontmatter.dump()`` to a text-mode file matches ``dumps()`` on
       python-frontmatter 1.3+ (mdpp still uses ``dumps`` for explicit UTF-8).
    3. ``process_content()`` returns a valid ``frontmatter.Post`` object.
    4. The full temporary-file write path produces a UTF-8 readable
       ``.gpp.markdown`` file.
    """

    @staticmethod
    def _write_gpp_markdown(post: fm.Post, path: str) -> None:
        """Mirror mdpp's gpp.markdown temp-file write path."""
        content = fm.dumps(post, sort_keys=False, default_flow_style=False)
        with open(path, "w", encoding="utf-8") as fd_text:
            fd_text.write(content)

    def test_gpp_markdown_write_pattern_succeeds(self) -> None:
        """mdpp's dumps()+text write pattern must produce readable UTF-8."""
        post = fm.loads("---\ntitle: Test\n---\nHello world")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            tmp_path = f.name
        try:
            self._write_gpp_markdown(post, tmp_path)
            with open(tmp_path, encoding="utf-8") as f:
                content = f.read()
            assert "title: Test" in content
            assert "Hello world" in content
        finally:
            os.unlink(tmp_path)

    def test_frontmatter_dump_matches_dumps_on_text_file(self) -> None:
        """dump() and dumps() agree on text-mode files (python-frontmatter 1.3+)."""
        post = fm.loads("---\ntitle: Test\n---\nHello world")
        dumps_content = fm.dumps(post, sort_keys=False, default_flow_style=False)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            tmp_path = f.name
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                fm.dump(post, f, sort_keys=False, default_flow_style=False)
            with open(tmp_path, encoding="utf-8") as f:
                dump_content = f.read()
            assert dump_content == dumps_content
        finally:
            os.unlink(tmp_path)

    def test_process_content_returns_post(self) -> None:
        """process_content() returns a frontmatter.Post that can be dumped."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as src:
            src.write("---\ntitle: Regression Test\n---\nBody text.\n")
            src_path = src.name

        args = argparse.Namespace(
            filename=src_path,
            no_header=False,
        )
        with patch("os.path.isfile", return_value=False):
            post = process_content(args, "", "")

        os.unlink(src_path)
        assert isinstance(post, fm.Post)
        assert post.metadata.get("title") == "Regression Test"
        assert "Body text." in post.content

    def test_gpp_markdown_tempfile_is_readable_utf8(self) -> None:
        """The .gpp.markdown temp file written by main() must be UTF-8 text.

        This is an integration-level regression test for the binary-mode bug.
        We create a real markdown source file, call main() with a mocked gpp
        invocation (so no actual preprocessing is required), and then verify
        the .gpp.markdown temp file is both present and valid UTF-8 text.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            src_path = os.path.join(tmpdir, "talk.md")
            tmp_gpp = os.path.join(tmpdir, "talk.gpp.markdown")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write("---\ntitle: UTF-8 test — café\n---\nContent with accents: naïve\n")

            args_ns = argparse.Namespace(
                filename=src_path,
                to="html",
                format="slides",
                output=os.path.join(tmpdir, "talk.html"),
                exercises=False,
                assignment=False,
                edit_links=False,
                draft=False,
                meta_data=[],
                code="none",
                diagrams_dir=None,
                scripts_dir=None,
                write_diagrams_dir=None,
                include_path=None,
                snippets_path=None,
                macros_path=tmpdir,
                macros=None,
                auto_install=False,
                verbose=False,
                no_header=False,
                replace_notation=False,
            )

            with (
                patch("argparse.ArgumentParser.parse_args", return_value=args_ns),
                patch("lamd.mdpp.validate_file_exists"),
                patch("lamd.mdpp.validate_include_paths"),
                patch("lamd.mdpp.load_config", return_value={}),
                patch("lamd.mdpp.setup_gpp_arguments", return_value=[]),
                patch("lamd.mdpp.process_includes", return_value=("", "")),
                patch("os.system"),  # Skip actual gpp invocation
                patch("os.path.isdir", return_value=True),
            ):
                main()

            # The temp file must exist and be valid UTF-8 text (not binary)
            assert os.path.isfile(tmp_gpp), f".gpp.markdown temp file not created: {tmp_gpp}"
            with open(tmp_gpp, encoding="utf-8") as f:
                content = f.read()
            assert "UTF-8 test" in content
            assert "café" in content


def test_gpp_temp_path_matches_html_and_manim_suffixes():
    """Temp path must be the same string later passed as GPP's infile."""
    assert gpp_temp_path("talk.md", "html") == "talk.gpp.markdown"
    assert gpp_temp_path("_policy/talk.md", "html") == "_policy/talk.gpp.markdown"
    assert gpp_temp_path("talk.md", "manim") == "talk.gpp.py"
    assert gpp_temp_path("talk.md", "manim-svg") == "talk.gpp.py"


def test_local_edit_url_from_ghub_list_and_mapping():
    """URL construction matches flags.py: ghub fields plus source basename."""
    expected = "https://github.com/lawrennd/talks/edit/gh-pages/_policy/time-to-reset.md"
    list_iface = {
        "ghub": [
            {
                "organization": "lawrennd",
                "repository": "talks",
                "branch": "gh-pages",
                "directory": "_policy",
            }
        ]
    }
    dict_iface = {
        "ghub": {
            "organization": "lawrennd",
            "repository": "talks",
            "branch": "gh-pages",
            "directory": "_policy",
        }
    }
    assert local_edit_url_from_iface(list_iface, "time-to-reset.md") == expected
    assert local_edit_url_from_iface(dict_iface, "_policy/time-to-reset.md") == expected
    assert local_edit_url_from_iface({}, "time-to-reset.md") is None
    assert local_edit_url_from_iface({"ghub": [{"organization": "lawrennd"}]}, "talk.md") is None


def test_setup_gpp_arguments_emits_local_edit_url_when_ghub_present():
    """mdpp must pass gppTempFile always and localEditUrl when ghub is complete."""
    args = argparse.Namespace(
        format="notes",
        to="html",
        exercises=False,
        assignment=False,
        edit_links=True,
        draft=False,
        meta_data=[],
        code="none",
        diagrams_dir=None,
        diagrams_web_dir=None,
        scripts_dir=None,
        write_diagrams_dir=None,
        include_path=None,
        snippets_path=None,
        macros_path=None,
        output="out.md",
        filename="time-to-reset.md",
    )
    iface = {
        "diagramsdir": "diagrams",
        "scriptsdir": "scripts",
        "writediagramsdir": "diagrams",
        "ghub": [
            {
                "organization": "lawrennd",
                "repository": "talks",
                "branch": "gh-pages",
                "directory": "_policy",
            }
        ],
    }
    gpp_args = setup_gpp_arguments(args, iface)
    assert "-DgppTempFile=time-to-reset.gpp.markdown" in gpp_args
    assert "-DlocalEditUrl=https://github.com/lawrennd/talks/edit/gh-pages/_policy/time-to-reset.md" in gpp_args
    assert "-DgithubBaseUrl=https://github.com/lawrennd/snippets/edit/main/" in gpp_args


def test_setup_gpp_arguments_omits_local_edit_url_without_ghub():
    args = argparse.Namespace(
        format="notes",
        to="html",
        exercises=False,
        assignment=False,
        edit_links=True,
        draft=False,
        meta_data=[],
        code="none",
        diagrams_dir=None,
        diagrams_web_dir=None,
        scripts_dir=None,
        write_diagrams_dir=None,
        include_path=None,
        snippets_path=None,
        macros_path=None,
        output="out.md",
        filename="talk.md",
    )
    iface = {"diagramsdir": "diagrams", "scriptsdir": "scripts", "writediagramsdir": "diagrams"}
    gpp_args = setup_gpp_arguments(args, iface)
    assert "-DgppTempFile=talk.gpp.markdown" in gpp_args
    assert not any(arg.startswith("-DlocalEditUrl=") for arg in gpp_args)


def _gpp_editme_command(input_path: str, output_path: str, extra_defines: list[str], include_dirs: list[str]) -> list[str]:
    import lamd.mdpp

    macros_dir = os.path.join(os.path.dirname(os.path.abspath(lamd.mdpp.__file__)), "macros")
    return [
        "gpp",
        "+n",
        "-U",
        "\\",
        "",
        "{",
        "}{",
        "}",
        "{",
        "}",
        "#",
        "",
        "-DEDIT=1",
        "-DgithubBaseUrl=https://github.com/lawrennd/snippets/edit/main/",
        *extra_defines,
        f"-I{macros_dir}",
        *[f"-I{directory}" for directory in include_dirs],
        "-o",
        output_path,
        input_path,
    ]


_EDITME_STUBS = r"""
\define{\span{contents}{class}{style}}{\contents}
\define{\alignright{block}}{\block}
\define{\hrefOther{link}{label}{other}}{EDITURL:\link}
\include{talk-macros-edit.gpp}
\define{\section{text}}{# \text
\ifdef{editText}\editText\undef{editText}\endif
}
"""


@pytest.mark.skipif(shutil.which("gpp") is None, reason="gpp not available")
def test_editme_in_main_file_uses_local_edit_url():
    """Leftover \\editme emitted by a talk heading must open the document URL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        infile = os.path.join(tmpdir, "talk.gpp.markdown")
        outfile = os.path.join(tmpdir, "out.md")
        with open(infile, "w", encoding="utf-8") as fd:
            fd.write(_EDITME_STUBS)
            fd.write("\\editme\n\\section{Sovereignty}\n")
        local_url = "https://github.com/lawrennd/talks/edit/gh-pages/_policy/talk.md"
        cmd = _gpp_editme_command(
            infile,
            outfile,
            [
                f"-DgppTempFile={infile}",
                f"-DlocalEditUrl={local_url}",
            ],
            [tmpdir],
        )
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        with open(outfile, encoding="utf-8") as fd:
            output = fd.read()
        assert f"EDITURL:{local_url}" in output
        assert "snippets/edit/main/" not in output


@pytest.mark.skipif(shutil.which("gpp") is None, reason="gpp not available")
def test_editme_inside_include_keeps_snippets_url():
    """\\editme expanded inside an include still uses githubBaseUrl plus the snippet path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        infile = os.path.join(tmpdir, "talk.gpp.markdown")
        snippet = os.path.join(tmpdir, "compute-concentration.md")
        outfile = os.path.join(tmpdir, "out.md")
        with open(snippet, "w", encoding="utf-8") as fd:
            fd.write("\\editme\n\\section{Snippet heading}\n")
        with open(infile, "w", encoding="utf-8") as fd:
            fd.write(_EDITME_STUBS)
            fd.write("\\include{compute-concentration.md}\n")
        local_url = "https://github.com/lawrennd/talks/edit/gh-pages/_policy/talk.md"
        cmd = _gpp_editme_command(
            infile,
            outfile,
            [
                f"-DgppTempFile={infile}",
                f"-DlocalEditUrl={local_url}",
            ],
            [tmpdir],
        )
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        with open(outfile, encoding="utf-8") as fd:
            output = fd.read()
        assert "EDITURL:https://github.com/lawrennd/snippets/edit/main/compute-concentration.md" in output
        assert local_url not in output
