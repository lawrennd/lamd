"""
Unit tests for the dependencies module.
"""

import os
import sys
import tempfile
from unittest.mock import patch

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from lamd.dependencies import main


class TestDependencies:
    """Test suite for the dependencies module."""

    def setup_method(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create a test markdown file with dependencies
        self.test_md_content = r"""---
title: Test Document
author: Test Author
---

# Introduction

\include{introduction.md}

\figure{\diagramsDir/example-diagram}{An example diagram}{example-diagram}

Here's a citation \cite{Smith2020}.

\includesvg{\diagramsDir/svg-diagram}{A SVG diagram}{svg-diagram}
\includediagram{\diagramsDir/diagram-file}{A regular diagram}{diagram-file}
\includepdf{\diagramsDir/pdf-diagram}{A PDF diagram}{pdf-diagram}
\includeimg{\diagramsDir/img-diagram}{An image diagram}{img-diagram}

\thanks
"""
        self.test_md_path = os.path.join(self.temp_dir.name, "test.md")
        with open(self.test_md_path, "w") as f:
            f.write(self.test_md_content)

        # Create test directories and files
        self.diagrams_dir = os.path.join(self.temp_dir.name, "diagrams")
        os.makedirs(self.diagrams_dir, exist_ok=True)

        # Create sample diagram files
        for filename in ["example-diagram.png", "svg-diagram.svg", "diagram-file.png", "pdf-diagram.pdf", "img-diagram.png"]:
            with open(os.path.join(self.diagrams_dir, filename), "w") as f:
                f.write("Test file content")

        # Create sample snippet
        self.snippets_dir = os.path.join(self.temp_dir.name, "snippets")
        os.makedirs(self.snippets_dir, exist_ok=True)
        with open(os.path.join(self.snippets_dir, "introduction.md"), "w") as f:
            f.write("This is an introduction snippet.")

        # Create sample bibliography
        with open(os.path.join(self.temp_dir.name, "references.bib"), "w") as f:
            f.write(
                """@article{Smith2020,
  author  = {Smith, John},
  title   = {Example Paper},
  journal = {Journal of Examples},
  year    = {2020},
  volume  = {1},
  pages   = {1--10}
}"""
            )

        # Create a patch for opening the test file
        # This is needed for tests that don't use the temp directory
        self.open_patcher = patch("builtins.open", create=True)
        self.mock_open = self.open_patcher.start()

    def teardown_method(self):
        """Clean up after each test."""
        # Remove temporary directory and its contents
        self.temp_dir.cleanup()

        # Stop the open patch
        self.open_patcher.stop()

    @patch("sys.argv", ["dependencies", "all", "test.md"])
    @patch("lynguine.util.talk.extract_all")
    @patch("lynguine.util.yaml.header_fields")
    @patch("lynguine.util.yaml.header_field")
    @patch("lynguine.util.yaml.Interface.from_file")
    @patch("builtins.print")
    def test_extract_all(self, mock_print, mock_interface, mock_header_field, mock_header_fields, mock_extract_all):
        """Test the 'all' dependency extraction."""
        # Mock the header_fields function to return a dictionary
        mock_header_fields.return_value = {"title": "Test Document"}

        # Mock the header_field function to return False for 'posts'
        mock_header_field.return_value = False

        # Mock the extract_all function to return a predefined list of files
        mock_extract_all.return_value = ["introduction.md", "diagrams/example-diagram.png", "references.bib"]

        # Call the main function
        main()

        # Verify extract_all was called with the correct arguments
        mock_extract_all.assert_called_once_with("test.md", user_file=["_lamd.yml", "_config.yml"])

        # Verify the output
        mock_print.assert_called_once_with("introduction.md diagrams/example-diagram.png references.bib")

    @patch("sys.argv", ["dependencies", "diagrams", "test.md", "-d", "/path/to/diagrams"])
    @patch("lynguine.util.talk.extract_diagrams")
    @patch("builtins.print")
    def test_extract_diagrams_with_custom_dir(self, mock_print, mock_extract_diagrams):
        """Test diagram extraction with custom diagrams directory."""
        # Mock extract_diagrams to return a predefined list
        mock_extract_diagrams.return_value = ["/path/to/diagrams/example-diagram.png", "/path/to/diagrams/svg-diagram.svg"]

        # Call the main function
        main()

        # Verify extract_diagrams was called with the correct arguments
        mock_extract_diagrams.assert_called_once_with("test.md", diagrams_dir="/path/to/diagrams", snippets_path="..")

        # Verify the output
        mock_print.assert_called_once_with("/path/to/diagrams/example-diagram.png /path/to/diagrams/svg-diagram.svg")

    @patch("sys.argv", ["dependencies", "slidediagrams", "test.md"])
    @patch("lynguine.util.talk.extract_diagrams")
    @patch("builtins.print")
    def test_extract_slidediagrams(self, mock_print, mock_extract_diagrams):
        """Test slide diagram extraction (SVG only)."""
        # Mock extract_diagrams to return a predefined list
        mock_extract_diagrams.return_value = ["diagrams/svg-diagram.svg"]

        # Call the main function
        main()

        # Verify extract_diagrams was called with the correct arguments
        mock_extract_diagrams.assert_called_once_with(
            "test.md",
            absolute_path=False,
            diagram_exts=["svg"],
            diagrams_dir="/Users/neil/lawrennd/slides/diagrams",
            snippets_path="..",
        )

        # Verify the output
        mock_print.assert_called_once_with("diagrams/svg-diagram.svg")

    @patch("sys.argv", ["dependencies", "texdiagrams", "test.md"])
    @patch("lynguine.util.talk.extract_diagrams")
    @patch("builtins.print")
    def test_extract_texdiagrams(self, mock_print, mock_extract_diagrams):
        """Test TeX diagram extraction (PDF only)."""
        # Mock extract_diagrams to return a predefined list
        mock_extract_diagrams.return_value = ["diagrams/pdf-diagram.pdf"]

        # Call the main function
        main()

        # Verify extract_diagrams was called with the correct arguments
        mock_extract_diagrams.assert_called_once_with(
            "test.md",
            absolute_path=False,
            diagram_exts=["pdf"],
            diagrams_dir="/Users/neil/lawrennd/slides/diagrams",
            snippets_path="..",
        )

        # Verify the output
        mock_print.assert_called_once_with("diagrams/pdf-diagram.pdf")

    @patch("sys.argv", ["dependencies", "docxdiagrams", "test.md"])
    @patch("lynguine.util.talk.extract_diagrams")
    @patch("builtins.print")
    def test_extract_docxdiagrams(self, mock_print, mock_extract_diagrams):
        """Test Word diagram extraction (EMF only)."""
        # Mock extract_diagrams to return a predefined list
        mock_extract_diagrams.return_value = ["diagrams/example-diagram.emf"]

        # Call the main function
        main()

        # Verify extract_diagrams was called with the correct arguments
        mock_extract_diagrams.assert_called_once_with(
            "test.md",
            absolute_path=False,
            diagram_exts=["emf"],
            diagrams_dir="/Users/neil/lawrennd/slides/diagrams",
            snippets_path="..",
        )

        # Verify the output
        mock_print.assert_called_once_with("diagrams/example-diagram.emf")

    @patch("sys.argv", ["dependencies", "inputs", "test.md", "-S", "/custom/snippets"])
    @patch("lynguine.util.talk.extract_inputs")
    @patch("builtins.print")
    def test_extract_inputs_with_custom_path(self, mock_print, mock_extract_inputs):
        """Test input extraction with custom snippets path."""
        # Mock extract_inputs to return a predefined list
        mock_extract_inputs.return_value = ["/custom/snippets/introduction.md"]

        # Call the main function
        main()

        # Verify extract_inputs was called with the correct arguments
        mock_extract_inputs.assert_called_once_with("test.md", snippets_path="/custom/snippets")

        # Verify the output
        mock_print.assert_called_once_with("/custom/snippets/introduction.md")

    @patch("sys.argv", ["dependencies", "inputs", "test.md"])
    @patch("lynguine.util.talk.extract_inputs")
    @patch("builtins.print")
    def test_extract_inputs_empty(self, mock_print, mock_extract_inputs):
        """Test input extraction with no results."""
        # Mock extract_inputs to return an empty list
        mock_extract_inputs.return_value = []

        # Call the main function
        main()

        # Verify extract_inputs was called
        mock_extract_inputs.assert_called_once()

        # Verify the output is an empty string
        mock_print.assert_called_once_with("")

    @patch("sys.argv", ["dependencies", "bibinputs", "test.md"])
    @patch("lynguine.util.talk.extract_bibinputs")
    @patch("builtins.print")
    def test_extract_bibinputs(self, mock_print, mock_extract_bibinputs):
        """Test bibliography input extraction."""
        # Mock extract_bibinputs to return a predefined list
        mock_extract_bibinputs.return_value = ["references.bib"]

        # Call the main function
        main()

        # Verify extract_bibinputs was called with the correct arguments
        mock_extract_bibinputs.assert_called_once_with("test.md")

        # Verify the output
        mock_print.assert_called_once_with("references.bib")

    @patch("sys.argv", ["dependencies", "batch", "test.md", "-S", "/custom/snippets", "-d", "/path/to/diagrams"])
    @patch("lynguine.util.talk.extract_inputs")
    @patch("lynguine.util.talk.extract_diagrams")
    @patch("lynguine.util.talk.extract_all")
    @patch("lynguine.util.yaml.header_fields")
    @patch("lynguine.util.yaml.header_field")
    @patch("lynguine.util.yaml.Interface.from_file")
    @patch("builtins.print")
    def test_batch_extraction(self, mock_print, mock_interface, mock_header_field, mock_header_fields, 
                             mock_extract_all, mock_extract_diagrams, mock_extract_inputs):
        """Test batch dependency extraction (CIP-0009 Phase 1)."""
        # Mock the inputs extraction
        mock_extract_inputs.return_value = ["/custom/snippets/intro.md", "/custom/snippets/conclusion.md"]
        
        # Mock the diagrams extraction (includes svg, png, pdf, emf)
        mock_extract_diagrams.return_value = [
            "/path/to/diagrams/example.svg",
            "/path/to/diagrams/example.png", 
            "/path/to/diagrams/example.pdf",
            "/path/to/diagrams/example.emf",
            "/path/to/diagrams/another.svg"
        ]
        
        # Mock the dynamic dependencies extraction
        mock_header_fields.return_value = {"title": "Test Document"}
        mock_header_field.return_value = False
        mock_extract_all.return_value = ["test.posts.html", "test.slides.html"]
        
        # Call the main function
        main()
        
        # Verify all extraction functions were called
        mock_extract_inputs.assert_called_once_with("test.md", snippets_path="/custom/snippets")
        mock_extract_diagrams.assert_called_once_with(
            "test.md",
            absolute_path=True,
            diagram_exts=['svg', 'png', 'pdf', 'emf'],
            diagrams_dir="/path/to/diagrams",
            snippets_path="/custom/snippets"
        )
        mock_extract_all.assert_called_once_with("test.md", user_file=["_lamd.yml", "_config.yml"])
        
        # Verify the output format (prefixed lines with dependency type names)
        calls = mock_print.call_args_list
        assert len(calls) == 6
        
        # Check each line starts with the correct prefix (dependency type names, not Makefile variables)
        assert calls[0][0][0].startswith("inputs:")
        assert calls[1][0][0].startswith("diagrams:")
        assert calls[2][0][0].startswith("docxdiagrams:")
        assert calls[3][0][0].startswith("pptxdiagrams:")
        assert calls[4][0][0].startswith("texdiagrams:")
        assert calls[5][0][0].startswith("all:")
        
        # Verify content
        assert "/custom/snippets/intro.md" in calls[0][0][0]
        assert "/custom/snippets/conclusion.md" in calls[0][0][0]
        assert "/path/to/diagrams/example.svg" in calls[1][0][0]
        assert "/path/to/diagrams/example.emf" in calls[2][0][0]
        assert "/path/to/diagrams/example.pdf" in calls[4][0][0]
        assert "test.posts.html" in calls[5][0][0]
        assert "test.slides.html" in calls[5][0][0]

    @patch("sys.argv", ["dependencies", "batch", "nonexistent.md"])
    @patch("lynguine.util.talk.extract_inputs")
    @patch("lynguine.util.talk.extract_diagrams")
    @patch("lynguine.util.talk.extract_all")
    @patch("lynguine.util.yaml.header_fields")
    @patch("lynguine.util.yaml.header_field")
    @patch("builtins.print")
    def test_batch_extraction_with_none_diagrams(self, mock_print, mock_header_field, mock_header_fields,
                                                  mock_extract_all, mock_extract_diagrams, mock_extract_inputs):
        """Test batch extraction handles None return from extract_diagrams (file doesn't exist)."""
        # Mock inputs extraction
        mock_extract_inputs.return_value = []
        
        # Mock extract_diagrams returning None (file doesn't exist)
        mock_extract_diagrams.return_value = None
        
        # Mock dynamic dependencies
        mock_header_fields.return_value = {"title": "Test"}
        mock_header_field.return_value = False
        mock_extract_all.return_value = []
        
        # Call the main function - should not raise an error
        main()
        
        # Verify output contains empty values for diagram types
        calls = mock_print.call_args_list
        assert len(calls) == 6
        
        # All diagram-related lines should be empty (just the prefix with dependency type names)
        assert calls[1][0][0] == "diagrams:"
        assert calls[2][0][0] == "docxdiagrams:"
        assert calls[3][0][0] == "pptxdiagrams:"
        assert calls[4][0][0] == "texdiagrams:"

    # Note: There's no extract_snippets function in lynguine.util.talk module,
    # but the code in dependencies.py refers to it. This test is left
    # commented out until the function is implemented or the code is fixed.

    # @patch('sys.argv', ['dependencies', 'snippets', 'test.md'])
    # @patch('lynguine.util.talk.extract_snippets')
    # @patch('builtins.print')
    # def test_extract_snippets(self, mock_print, mock_extract_snippets):
    #     """Test snippet extraction."""
    #     # Mock extract_snippets to return a predefined list
    #     mock_extract_snippets.return_value = ['introduction.md']
    #
    #     # Call the main function
    #     main()
    #
    #     # Verify extract_snippets was called with the correct arguments
    #     mock_extract_snippets.assert_called_once_with(
    #         'test.md',
    #         absolute_path=False,
    #         snippets_path='..'
    #     )
    #
    #     # Verify the output
    #     mock_print.assert_called_once_with('introduction.md')
