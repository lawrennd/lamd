"""The Jekyll talk template must emit YAML-safe titles and abstracts.

Pandoc turns ``$F = U - TS$`` or ``$M/M/1$`` into HTML with
``class="math inline"``. A double-quoted YAML field then loses ``layout``
and ``week``, so Jekyll renders the page without the site header.
"""

import textwrap
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

TEMPLATE = Path(__file__).resolve().parents[2] / "lamd/templates/pandoc/pandoc-jekyll-talk-template.html"


def _load_frontmatter(text: str) -> dict:
    rest = text[3:]
    end = rest.find("\n---")
    assert end != -1
    return yaml.safe_load(rest[:end])


def test_quoted_abstract_with_math_span_is_invalid_yaml():
    broken = textwrap.dedent("""\
        ---
        title: "Motivation"
        abstract: "<p>The free-energy decomposition <span class="math inline">\\(F = U - TS\\)</span>.</p>"
        week: 1
        layout: lecture
        ---
        """)
    with pytest.raises(yaml.YAMLError):
        _load_frontmatter(broken)


def test_literal_abstract_with_math_span_keeps_week_and_layout():
    html = "<p>The free-energy decomposition " '<span class="math inline">\\(F = U - TS\\)</span>.</p>'
    text = textwrap.dedent(f"""\
        ---
        title: "Motivation"
        abstract: |-
          {html}
        week: 1
        layout: lecture
        ---
        """)
    data = _load_frontmatter(text)
    assert data["week"] == 1
    assert data["layout"] == "lecture"
    assert 'class="math inline"' in data["abstract"]
    assert "F = U - TS" in data["abstract"]


def test_quoted_title_with_math_span_is_invalid_yaml():
    broken = textwrap.dedent("""\
        ---
        title: "Lab 1: Discrete Simulation of the <span class="math inline">\\(M/M/1\\)</span> Queue"
        week: 3
        layout: practical
        ---
        """)
    with pytest.raises(yaml.YAMLError):
        _load_frontmatter(broken)


def test_literal_title_with_math_span_keeps_week_and_layout():
    html = "Lab 1: Discrete Simulation of the " '<span class="math inline">\\(M/M/1\\)</span> Queue'
    text = textwrap.dedent(f"""\
        ---
        title: |-
          {html}
        week: 3
        layout: practical
        ---
        """)
    data = _load_frontmatter(text)
    assert data["week"] == 3
    assert data["layout"] == "practical"
    assert 'class="math inline"' in data["title"]
    assert "M/M/1" in data["title"]


def test_talk_template_uses_literal_blocks_for_title_and_abstract():
    template = TEMPLATE.read_text()
    assert "title: |-" in template
    assert 'title: "$title$"' not in template
    assert "abstract: |-" in template
