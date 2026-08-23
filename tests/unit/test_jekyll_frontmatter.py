"""The Jekyll talk template must emit YAML-safe abstracts.

Pandoc turns ``$F = U - TS$`` into HTML with ``class="math inline"``.
A double-quoted YAML abstract then loses ``layout`` and ``week``.
"""

import textwrap

import pytest

yaml = pytest.importorskip("yaml")


def _load_frontmatter(text: str) -> dict:
    rest = text[3:]
    end = rest.find("\n---")
    assert end != -1
    return yaml.safe_load(rest[:end])


def test_quoted_abstract_with_math_span_is_invalid_yaml():
    broken = textwrap.dedent(
        """\
        ---
        title: "Motivation"
        abstract: "<p>The free-energy decomposition <span class="math inline">\\(F = U - TS\\)</span>.</p>"
        week: 1
        layout: lecture
        ---
        """
    )
    with pytest.raises(yaml.YAMLError):
        _load_frontmatter(broken)


def test_literal_abstract_with_math_span_keeps_week_and_layout():
    html = "<p>The free-energy decomposition " '<span class="math inline">\\(F = U - TS\\)</span>.</p>'
    text = textwrap.dedent(
        f"""\
        ---
        title: "Motivation"
        abstract: |-
          {html}
        week: 1
        layout: lecture
        ---
        """
    )
    data = _load_frontmatter(text)
    assert data["week"] == 1
    assert data["layout"] == "lecture"
    assert 'class="math inline"' in data["abstract"]
    assert "F = U - TS" in data["abstract"]
