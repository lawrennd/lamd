"""Makefile-chain tests for CV list scanning and reference-doc checks."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import pytest

import lamd

MAKEFILES = Path(lamd.__file__).resolve().parent / "makefiles"
FIND = "gfind" if subprocess.run(["which", "gfind"], capture_output=True).returncode == 0 else "find"


def _run_make(cwd: Path, *targets: str, extra: str = "") -> subprocess.CompletedProcess[str]:
    makefile = cwd / "Makefile"
    cmd = ["make", "-f", str(makefile), f"FIND={FIND}"]
    if extra:
        cmd.extend(extra.split())
    cmd.extend(targets)
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def test_colon_in_talksdir_does_not_crash_make_parse(tmp_path: Path) -> None:
    """GNU Make must not see colon paths as static-pattern prerequisites."""
    talks = tmp_path / "talks" / "_notebooks"
    talks.mkdir(parents=True)
    (talks / "https:example.gif").write_bytes(b"gif")
    (talks / "a-talk.md").write_text("# talk\n")

    makefile = tmp_path / "Makefile"
    makefile.write_text(f"""
TALKSDIR={talks}
TALKSINCE=2020
MAKEFILESDIR={MAKEFILES}
include $(MAKEFILESDIR)/make-lists.mk

.PHONY: all
all: invited-talk-list.markdown
""")

    listed = _run_make(tmp_path, "-n", "all")
    assert listed.returncode == 0, listed.stderr
    assert "multiple target patterns" not in listed.stderr


def test_talksdir_posts_is_preferred_over_lecture_notes(tmp_path: Path) -> None:
    """If talks/_posts exists, do not scan lecture notes beside it."""
    talks = tmp_path / "talks"
    posts = talks / "_posts"
    posts.mkdir(parents=True)
    invited = posts / "2024-01-01-invited.md"
    invited.write_text("---\ntitle: Invited\nvenue: Somewhere\n---\n")
    (talks / "lecture-note.md").write_text("---\ntitle: Lecture\nabstract: skip\n---\n")
    stub = tmp_path / "mdlist"
    stub.write_text("#!/bin/sh\nprintf '%s\\n' \"$@\" > mdlist-args.txt\n")
    stub.chmod(0o755)
    makefile = tmp_path / "Makefile"
    makefile.write_text(f"""
TALKSDIR={talks}
TALKSINCE=2020
MAKEFILESDIR={MAKEFILES}
include $(MAKEFILESDIR)/make-lists.mk
""")
    env = os.environ.copy()
    env["PATH"] = f"{tmp_path}:{env.get('PATH', '')}"
    result = subprocess.run(
        ["make", "-f", str(makefile), f"FIND={FIND}", "invited-talk-list.markdown"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, result.stderr
    args = (tmp_path / "mdlist-args.txt").read_text()
    assert "2024-01-01-invited.md" in args
    assert "lecture-note.md" not in args


def test_empty_talks_posts_does_not_scan_cwd_or_siblings(tmp_path: Path) -> None:
    talks = tmp_path / "talks"
    (talks / "_posts").mkdir(parents=True)
    (talks / "sibling.md").write_text("not a talk post")
    (tmp_path / "stray.md").write_text("cwd")
    makefile = tmp_path / "Makefile"
    makefile.write_text(f"""
TALKSDIR={talks}
TALKSINCE=2020
MAKEFILESDIR={MAKEFILES}
include $(MAKEFILESDIR)/make-lists.mk
""")
    result = _run_make(tmp_path, "invited-talk-list.markdown")
    assert result.returncode == 0, result.stderr
    out = (tmp_path / "invited-talk-list.markdown").read_text()
    assert out == ""
    assert "sibling" not in out
    assert "stray" not in out


def test_empty_talksdir_does_not_find_cwd(tmp_path: Path) -> None:
    """Unset TALKSDIR must not make find search the CV directory."""
    (tmp_path / "stray.md").write_text("should-not-be-scanned")
    makefile = tmp_path / "Makefile"
    makefile.write_text(f"""
TALKSDIR=
TALKSINCE=2020
MAKEFILESDIR={MAKEFILES}
include $(MAKEFILESDIR)/make-lists.mk
""")
    result = _run_make(tmp_path, "invited-talk-list.markdown")
    assert result.returncode == 0, result.stderr
    out = tmp_path / "invited-talk-list.markdown"
    assert out.exists()
    assert out.read_text() == ""
    assert "stray.md" not in out.read_text()


def test_cv_flags_do_not_shell_find_at_parse_time() -> None:
    text = (MAKEFILES / "make-cv-flags.mk").read_text()
    assert "$(shell ${FIND}" not in text
    assert "$(shell $(FIND)" not in text
    assert "make-check-reference-docs.mk" in text


def test_check_reference_docs_exists_on_cv_flag_chain(tmp_path: Path) -> None:
    makefile = tmp_path / "Makefile"
    makefile.write_text(f"""
BASE=cv
MAKEFILESDIR={MAKEFILES}
include $(MAKEFILESDIR)/make-check-reference-docs.mk
""")
    result = _run_make(tmp_path, "-n", "check-reference-docs")
    assert result.returncode == 0, result.stderr
    assert "No rule to make target" not in result.stderr


def test_missing_reference_doc_fails_fast(tmp_path: Path) -> None:
    """If flags emit --reference-doc for a missing file, the check exits 1."""
    stub_flags = tmp_path / "flags"
    stub_flags.write_text("""#!/bin/sh
if [ "$1" = "docx" ]; then
  echo "--reference-doc /definitely/missing/custom-reference.dotx"
fi
""")
    stub_flags.chmod(0o755)
    makefile = tmp_path / "Makefile"
    makefile.write_text(f"""
BASE=cv
MAKEFILESDIR={MAKEFILES}
include $(MAKEFILESDIR)/make-check-reference-docs.mk
""")
    env = os.environ.copy()
    env["PATH"] = f"{tmp_path}:{env.get('PATH', '')}"
    result = subprocess.run(
        ["make", "-f", str(makefile), "check-reference-docs"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode != 0
    combined = result.stdout + result.stderr
    assert "reference template not found" in combined


def test_cv_compile_blockers_cleared_for_pdf_work(tmp_path: Path) -> None:
    """Docx compile blockers are gone, so cvneil PDF work can start.

    A CV makefile with a colon in talksdir still parses, check-reference-docs
    exists on the CV chain, and make-cv.mk still only asks for docx today.
    """
    talks = tmp_path / "talks"
    talks.mkdir()
    (talks / "https:example.gif").write_bytes(b"gif")
    makefile = tmp_path / "Makefile"
    makefile.write_text(f"""
TALKSDIR={talks}
TALKSINCE=2020
BASE=cv
MAKEFILESDIR={MAKEFILES}
include $(MAKEFILESDIR)/make-lists.mk
include $(MAKEFILESDIR)/make-check-reference-docs.mk

.PHONY: all
all: check-reference-docs invited-talk-list.markdown
""")
    result = _run_make(tmp_path, "-n", "all")
    assert result.returncode == 0, result.stderr
    assert "multiple target patterns" not in result.stderr
    assert "No rule to make target" not in result.stderr

    cv_mk = (MAKEFILES / "make-cv.mk").read_text()
    assert "$(MAKE) $(BASE).docx" in cv_mk
    makecv_src = Path(lamd.__file__).resolve().parent / "makecv.py"
    assert "subprocess.run" in makecv_src.read_text()


@pytest.mark.xfail(strict=True, reason="Honour pdf: true via cvneil (backlog 2026-10-22_cv-pdf-via-cvneil)")
def test_pdf_true_make_all_requests_cvneil_pdf() -> None:
    """When frontmatter has pdf: true, all must build ${BASE}.pdf with cvneil.

    Not the talks notes PDF. No LaTeX run here: this is the makefile contract
    the cvneil task should satisfy.
    """
    cv_mk = (MAKEFILES / "make-cv.mk").read_text()
    active = [line for line in cv_mk.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    pdf_lines = [line for line in active if re.search(r"\$[\({]BASE[\)}]\.pdf", line) and "notes.pdf" not in line]
    assert pdf_lines, "make-cv.mk all should request ${BASE}.pdf when pdf is enabled"
    joined = "\n".join(pdf_lines) + "\n" + cv_mk
    assert "cvneil" in joined.lower() or "pandoc-cv" in joined.lower()
