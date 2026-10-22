"""Make wrappers must return Make's exit code, not an os.system wait status."""

from __future__ import annotations

import subprocess
from unittest.mock import patch

from lamd.makecv import main as makecv_main
from lamd.maketalk import main as maketalk_main


def test_makecv_propagates_make_returncode(monkeypatch, tmp_path) -> None:
    cv = tmp_path / "cv.md"
    cv.write_text("---\ntitle: t\ndocx: true\n---\n\n# CV\n")
    (tmp_path / "_lamd.yml").write_text(
        f"snippetsdir: {tmp_path / 'snippets'}\n" f"bibdir: {tmp_path / 'bib'}\n" f"postsdir: {tmp_path / 'posts'}\n"
    )
    (tmp_path / "snippets").mkdir()
    (tmp_path / "bib").mkdir()
    (tmp_path / "posts").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["makecv", "cv.md"])

    completed = subprocess.CompletedProcess(args=["make", "all"], returncode=2)
    with patch("lamd.makecv.subprocess.run", return_value=completed) as mocked:
        assert makecv_main() == 2
        mocked.assert_called()
        args, kwargs = mocked.call_args
        assert args[0] == ["make", "all"]
        assert kwargs.get("check") is False


def test_maketalk_propagates_make_returncode(monkeypatch, tmp_path) -> None:
    talk = tmp_path / "talk.md"
    talk.write_text("---\ntitle: t\n---\n\n# Talk\n")
    (tmp_path / "_lamd.yml").write_text(
        f"snippetsdir: {tmp_path / 'snippets'}\n" f"bibdir: {tmp_path / 'bib'}\n" f"postsdir: {tmp_path / 'posts'}\n"
    )
    (tmp_path / "snippets").mkdir()
    (tmp_path / "bib").mkdir()
    (tmp_path / "posts").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["maketalk", "talk.md"])

    completed = subprocess.CompletedProcess(args=["make", "all"], returncode=2)
    with patch("lamd.maketalk.subprocess.run", return_value=completed) as mocked:
        assert maketalk_main() == 2
        assert mocked.call_args.kwargs.get("check") is False
        assert mocked.call_args.kwargs.get("shell") is True
        assert mocked.call_args.args[0].startswith("make")
