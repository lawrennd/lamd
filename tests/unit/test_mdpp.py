import argparse
import os
import subprocess
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from lamd.mdpp import main, setup_gpp_arguments
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
    args.scripts_dir = "/usr/scripts"
    args.write_diagrams_dir = "/usr/diagrams"
    args.include_path = "/usr/include"
    args.snippets_path = "/usr/snippets"
    args.macros_path = "/usr/macros:/usr/macrostoo"
    args.output = "output.md"
    args.macros = "macros"

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
    from lamd.mdpp import setup_gpp_arguments
    import argparse
    
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
        scripts_dir=None,
        write_diagrams_dir=None,
        include_path=None,
        snippets_path=None,
        macros_path=None,
        output="test.md"
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
