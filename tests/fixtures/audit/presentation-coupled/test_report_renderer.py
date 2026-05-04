"""Report renderer tests.

Fixture for the SLOBAC audit's `presentation-coupled` scenario. Two planted
positives assert on raw-string presentation; one negative control parses
the structured JSON layer and asserts on shape.
"""

from __future__ import annotations

import json


def render_status_html(name: str, status: str, count: int) -> str:
    """SUT — render a status row as HTML."""
    return (
        f'<div class="status-row" data-name="{name}">'
        f"<span class=\"status status-{status}\">{status.upper()}</span>"
        f"<span class=\"count\">{count}</span>"
        f"</div>"
    )


def render_status_json(name: str, status: str, count: int) -> str:
    """SUT — render the same status row as JSON."""
    return json.dumps({"name": name, "status": status, "count": count})


# --- positive 1: full-string equality on rendered HTML.                     -
#     Any cosmetic change (attribute ordering, whitespace, additional   -
#     class for theming, line breaks for readability) breaks this test -
#     even though the structural contract (figure wrapping a status    -
#     span and a count span) is preserved.                              -

def test_render_status_html_for_active_user():
    expected = (
        '<div class="status-row" data-name="alice">'
        '<span class="status status-active">ACTIVE</span>'
        '<span class="count">5</span>'
        "</div>"
    )
    assert render_status_html("alice", "active", 5) == expected


# --- positive 2: long `toContain` / `in` chain against rendered output.    -
#     Pins specific class names, exact ALLCAPS spelling of status, and  -
#     even the literal "data-name=" attribute — all cosmetic concerns.-

def test_render_status_html_includes_active_styling():
    html = render_status_html("bob", "active", 3)
    assert "status-active" in html
    assert "ACTIVE" in html
    assert 'data-name="bob"' in html
    assert "<span" in html
    assert "</div>" in html


# --- negative control: parse the structured layer; assert on shape.         -
#     `render_status_json` is the JSON-tier renderer for the same      -
#     status row. The test calls `json.loads` and asserts on the      -
#     parsed dict — a structural assertion that survives any pretty- -
#     printing or key-ordering change in the renderer's output.       -

def test_render_status_json_encodes_name_status_and_count():
    rendered = render_status_json("carol", "active", 7)
    parsed = json.loads(rendered)
    assert parsed == {"name": "carol", "status": "active", "count": 7}
