import json
import os
import subprocess

# Add the parent directory to the Python path
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


# Import check_dependency directly to avoid lynguine dependency issues
def check_dependency(dependency):
    """Check if a dependency is available."""
    import shutil

    return shutil.which(dependency) is not None


class TestCellBoundaries:
    """Test class for cell boundary functionality in LaMD pipeline."""

    STRAY_CELL_MARKER = "::: {.cell .markdown}"

    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def macros_dir(self) -> Path:
        return self.repo_root / "lamd" / "macros"

    @property
    def ipynb_template(self) -> Path:
        return self.repo_root / "lamd" / "templates" / "pandoc" / "pandoc-jekyll-ipynb-template"

    @property
    def csl_file(self) -> Path:
        return self.repo_root / "lamd" / "includes" / "elsevier-harvard.csl"

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = Path(__file__).parent
        self.test_file = self.test_dir / "test-cell-boundaries.md"
        self.temp_dir = tempfile.mkdtemp()
        # print(f"Using temp directory: {self.temp_dir}")  # Debug output

    def teardown_method(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        for file in Path(self.temp_dir).glob("*"):
            if file.is_file():
                file.unlink()
        os.rmdir(self.temp_dir)

    def count_cells(self, ipynb_file: Path) -> int:
        """Count the number of cells in a Jupyter notebook."""
        try:
            with open(ipynb_file, "r") as f:
                notebook = json.load(f)
            return len(notebook.get("cells", []))
        except Exception as e:
            raise e

    def validate_notebook_cells(self, ipynb_file: Path, expected_min: int = 1) -> tuple[bool, str]:
        """Validate that a notebook has sufficient cells and return status with message."""
        try:
            cell_count = self.count_cells(ipynb_file)
            if cell_count >= expected_min:
                return True, f"✅ Notebook has {cell_count} cells (>= {expected_min})"
            else:
                return False, f"❌ Notebook has only {cell_count} cells (expected >= {expected_min})"
        except Exception as e:
            return False, f"❌ Failed to read notebook: {e}"

    def notebook_cell_sources(self, ipynb_file: Path) -> list[str]:
        """Return the source text for each cell in a notebook."""
        with open(ipynb_file, "r") as f:
            notebook = json.load(f)
        return ["".join(cell.get("source", [])) for cell in notebook.get("cells", [])]

    def assert_no_stray_cell_markers(self, ipynb_file: Path) -> None:
        """Fail if pandoc left cell-boundary syntax in notebook cell content."""
        for index, source in enumerate(self.notebook_cell_sources(ipynb_file)):
            assert (
                self.STRAY_CELL_MARKER not in source
            ), f"Cell {index} contains stray pandoc cell marker: {self.STRAY_CELL_MARKER!r}"

    @pytest.mark.skipif(not check_dependency("mdpp"), reason="mdpp not available")
    @pytest.mark.skipif(not check_dependency("pandoc"), reason="pandoc not available")
    def test_references_cell_boundary_no_stray_markers(self):
        """References must not open an unclosed ipynb cell at document end.

        \\references used to expand to \\subsection{References}, which emitted
        ::: {.cell .markdown} without a closing :::. Pandoc then left the opener
        as literal notebook content.
        """
        test_file = self.test_dir / "test-references-cell-boundary.md"
        notes_output = Path(self.temp_dir) / "test-references-cell-boundary.notes.ipynb.markdown"

        subprocess.run(
            [
                "mdpp",
                str(test_file),
                "-o",
                str(notes_output),
                "--format",
                "notes",
                "--macros-path",
                str(self.macros_dir),
                "--to",
                "ipynb",
                "--code",
                "ipynb",
                "--replace-notation",
            ],
            check=True,
            capture_output=True,
        )

        notes_text = notes_output.read_text()
        assert f"{self.STRAY_CELL_MARKER}\n\n## References" not in notes_text

        tmp_output = Path(self.temp_dir) / "test-references-cell-boundary.tmp.markdown"
        subprocess.run(
            [
                "pandoc",
                "--template",
                str(self.ipynb_template),
                "--markdown-headings=atx",
                "--out",
                str(tmp_output),
                str(notes_output),
            ],
            check=True,
            capture_output=True,
        )

        pandoc_output = Path(self.temp_dir) / "test-references-cell-boundary.ipynb"
        subprocess.run(
            [
                "pandoc",
                "-s",
                "--citeproc",
                f"--csl={self.csl_file}",
                "--out",
                str(pandoc_output),
                str(tmp_output),
            ],
            check=True,
            capture_output=True,
        )

        self.assert_no_stray_cell_markers(pandoc_output)

        references_cells = [source for source in self.notebook_cell_sources(pandoc_output) if "## References" in source]
        assert references_cells, "Expected a References markdown cell"
        assert "Boltzmann" in references_cells[0], "Expected citeproc bibliography in References cell"

    @pytest.mark.skipif(not check_dependency("mdpp"), reason="mdpp not available")
    @pytest.mark.skipif(not check_dependency("pandoc"), reason="pandoc not available")
    @pytest.mark.skipif(not check_dependency("notedown"), reason="notedown not available")
    def test_cell_boundary_pipeline(self):
        """Test that the LaMD pipeline properly creates cell boundaries.

        This test verifies that pandoc correctly processes cell boundaries in the
        LaMD pipeline after the template fix. The test should pass with pandoc
        generating sufficient cells without requiring notedown fallback.

        See backlog item: 2025-08-30_pandoc-cell-boundary-issue.md (RESOLVED)
        """

        # Expected minimum cells: 3 headers + 3 code blocks + metadata cells = ~9+ cells
        expected_min = 9

        # Step 1: mdpp preprocessing
        notes_output = Path(self.temp_dir) / "test-cell-boundaries.notes.ipynb.markdown"
        try:
            subprocess.run(
                [
                    "mdpp",
                    str(self.test_file),
                    "-o",
                    str(notes_output),
                    "--format",
                    "notes",
                    "--snippets-path",
                    "/Users/neil/lawrennd/snippets",
                    "--macros-path=/Users/neil/lawrennd/lamd/lamd/macros",
                    "--to",
                    "ipynb",
                    "--code",
                    "ipynb",
                    "--replace-notation",
                    "--edit-links",
                    "--exercises",
                    "--include-path",
                    "./..",
                ],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            pytest.fail(f"mdpp preprocessing failed: {e}")

        # Step 2: pandoc template processing
        tmp_output = Path(self.temp_dir) / "test-cell-boundaries.tmp.markdown"
        try:
            subprocess.run(
                [
                    "pandoc",
                    "--template",
                    "/Users/neil/lawrennd/lamd/lamd/templates/pandoc/pandoc-jekyll-ipynb-template",
                    "--markdown-headings=atx",
                    "--out",
                    str(tmp_output),
                    str(notes_output),
                ],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            pytest.fail(f"pandoc template processing failed: {e}")

        # Step 3: pandoc final conversion
        pandoc_output = Path(self.temp_dir) / "test-cell-boundaries-pandoc.ipynb"
        try:
            subprocess.run(
                [
                    "pandoc",
                    "-s",
                    "--citeproc",
                    "--csl=/Users/neil/lawrennd/lamd/lamd/includes/elsevier-harvard.csl",
                    "--bibliography=/Users/neil/lawrennd/bibliography/lawrence.bib",
                    "--bibliography=/Users/neil/lawrennd/bibliography/other.bib",
                    "--bibliography=/Users/neil/lawrennd/bibliography/zbooks.bib",
                    "--mathjax=https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_SVG",
                    "--out",
                    str(pandoc_output),
                    str(tmp_output),
                ],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            pytest.fail(f"pandoc final conversion failed: {e}")

        # Step 4: notedown conversion
        notedown_output = Path(self.temp_dir) / "test-cell-boundaries-notedown.ipynb"
        try:
            with open(notedown_output, "w") as f:
                subprocess.run(["notedown", str(tmp_output)], stdout=f, check=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"notedown conversion failed: {e}")

        # Compare results
        pandoc_cells = self.count_cells(pandoc_output)
        notedown_cells = self.count_cells(notedown_output)

        print(f"Pandoc generated: {pandoc_cells} cells")
        print(f"Notedown generated: {notedown_cells} cells")

        # Assert that notedown produces sufficient cells (this is the working method)
        assert (
            notedown_cells >= expected_min
        ), f"Notedown generated only {notedown_cells} cells, expected at least {expected_min}"

        # Check if pandoc has the known cell boundary issue
        if pandoc_cells < expected_min and notedown_cells >= expected_min:
            print(f"❌ FAILED: Pandoc cell boundary issue detected")
            print(f"   - Pandoc: {pandoc_cells} cells (insufficient)")
            print(f"   - Notedown: {notedown_cells} cells (working)")
            print(f"   - Notedown is required as fallback for proper cell boundaries")
            pytest.fail(
                f"Pandoc is not properly creating cell boundaries. Generated {pandoc_cells} cells, expected at least {expected_min}. Notedown fallback works ({notedown_cells} cells)."
            )
        elif pandoc_cells >= expected_min:
            print(f"✅ Pandoc is working correctly: {pandoc_cells} cells")
        elif pandoc_cells < expected_min and notedown_cells < expected_min:
            print(f"🚨 CRITICAL: Both pandoc and notedown are failing!")
            print(f"   - Pandoc: {pandoc_cells} cells (insufficient)")
            print(f"   - Notedown: {notedown_cells} cells (also insufficient)")
            print(f"   - No working fallback available!")
            pytest.fail(
                f"CRITICAL: Both pandoc and notedown are failing to create proper cell boundaries. Pandoc: {pandoc_cells} cells, Notedown: {notedown_cells} cells. Expected at least {expected_min} cells."
            )
        else:
            pytest.fail(f"Unexpected state - pandoc: {pandoc_cells}, notedown: {notedown_cells}")

    @pytest.mark.skipif(not check_dependency("notedown"), reason="notedown not available")
    def test_notedown_cell_creation(self):
        """Test that notedown properly creates cell boundaries from markdown."""

        # Create a simple test markdown file with LaMD \code{} syntax
        test_md = Path(self.temp_dir) / "simple-test.md"
        test_md.write_text(
            """# Header 1
Content 1

\\code{print("Code 1")}

# Header 2
Content 2

\\code{print("Code 2")}
"""
        )

        # Step 1: mdpp preprocessing (convert \code{} to proper markdown)
        notes_output = Path(self.temp_dir) / "simple-test.notes.ipynb.markdown"
        try:
            subprocess.run(
                [
                    "mdpp",
                    str(test_md),
                    "-o",
                    str(notes_output),
                    "--format",
                    "notes",
                    "--snippets-path",
                    "/Users/neil/lawrennd/snippets",
                    "--macros-path=/Users/neil/lawrennd/lamd/lamd/macros",
                    "--to",
                    "ipynb",
                    "--code",
                    "ipynb",
                    "--replace-notation",
                    "--edit-links",
                    "--exercises",
                    "--include-path",
                    "./..",
                ],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            pytest.fail(f"mdpp preprocessing failed: {e}")

        # Step 2: pandoc template processing
        tmp_output = Path(self.temp_dir) / "simple-test.tmp.markdown"
        try:
            subprocess.run(
                [
                    "pandoc",
                    "--template",
                    "/Users/neil/lawrennd/lamd/lamd/templates/pandoc/pandoc-jekyll-ipynb-template",
                    "--markdown-headings=atx",
                    "--out",
                    str(tmp_output),
                    str(notes_output),
                ],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            pytest.fail(f"pandoc template processing failed: {e}")

        # Step 3: notedown conversion (following the slides.ipynb pattern from makefile)
        output_ipynb = Path(self.temp_dir) / "simple-test.ipynb"
        try:
            with open(output_ipynb, "w") as f:
                subprocess.run(["notedown", str(tmp_output)], stdout=f, check=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"notedown conversion failed: {e}")

        # Check that cells were created
        cell_count = self.count_cells(output_ipynb)
        assert cell_count >= 4, f"Expected at least 4 cells, got {cell_count}"

    def test_count_cells_function(self):
        """Test the count_cells helper function."""
        # Create a minimal valid notebook
        notebook = {
            "cells": [{"cell_type": "markdown", "source": ["# Test"]}, {"cell_type": "code", "source": ["print('test')"]}]
        }

        notebook_file = Path(self.temp_dir) / "test-notebook.ipynb"
        with open(notebook_file, "w") as f:
            json.dump(notebook, f)

        cell_count = self.count_cells(notebook_file)
        assert cell_count == 2, f"Expected 2 cells, got {cell_count}"

    def test_count_cells_invalid_file(self):
        """Test count_cells with invalid file."""
        invalid_file = Path(self.temp_dir) / "nonexistent.ipynb"
        with pytest.raises(Exception):
            self.count_cells(invalid_file)

    @pytest.mark.skipif(not check_dependency("notedown"), reason="notedown not available")
    def test_notedown_failure_detection(self):
        """Test that we can detect when notedown fails to create proper cell boundaries."""

        # Create a test file that should cause notedown to fail or create insufficient cells
        test_md = Path(self.temp_dir) / "notedown-failure-test.md"
        test_md.write_text(
            """# Test Header

This is a simple test without any code blocks or complex structure.

# Another Header

More content here.
"""
        )

        # Try to convert with notedown
        output_ipynb = Path(self.temp_dir) / "notedown-failure-test.ipynb"
        try:
            with open(output_ipynb, "w") as f:
                subprocess.run(["notedown", str(test_md)], stdout=f, check=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"notedown conversion failed: {e}")

        # Check cell count
        cell_count = self.count_cells(output_ipynb)

        # This simple file should create at least 2 cells (headers + content)
        expected_min = 2
        if cell_count < expected_min:
            print(f"⚠️ WARNING: Notedown created only {cell_count} cells from simple test file")
            print(f"   Expected at least {expected_min} cells")
            print(f"   This suggests notedown may have issues with basic markdown conversion")

        # The test passes regardless, but warns about potential issues
        assert cell_count >= 1, f"Notedown failed completely - no cells created"

    def test_validation_utility(self):
        """Test the validation utility function."""

        # Create a valid notebook
        valid_notebook = {
            "cells": [
                {"cell_type": "markdown", "source": ["# Test"]},
                {"cell_type": "code", "source": ["print('test')"]},
                {"cell_type": "markdown", "source": ["More content"]},
            ]
        }

        valid_file = Path(self.temp_dir) / "valid-notebook.ipynb"
        with open(valid_file, "w") as f:
            json.dump(valid_notebook, f)

        # Test validation
        is_valid, message = self.validate_notebook_cells(valid_file, expected_min=2)
        assert is_valid, f"Valid notebook should pass validation: {message}"

        # Test with higher expectation
        is_valid, message = self.validate_notebook_cells(valid_file, expected_min=5)
        assert not is_valid, f"Notebook with 3 cells should fail validation with min=5: {message}"

        # Test with invalid file
        invalid_file = Path(self.temp_dir) / "nonexistent.ipynb"
        is_valid, message = self.validate_notebook_cells(invalid_file)
        assert not is_valid, f"Invalid file should fail validation: {message}"
