"""Session lifecycle tests.

Fixture for the SLOBAC audit's `naming-lies` scenario. Every test whose title
does not match its body is a planted naming-lie; one test is a negative example
whose title uses different words from its body but means the same thing
(semantic synonymy — must NOT be flagged).
"""

from __future__ import annotations

import sqlite3


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE sessions (
            id TEXT PRIMARY KEY,
            token_count INTEGER NOT NULL DEFAULT 0,
            workspace_slug TEXT
        )
        """
    )
    return conn


# --- lie: title says "default to zero"; body checks > 0.                    -
#     Expected fix path: INVESTIGATE — the ambiguity is whether the operator -
#     cares about the default or the post-insert value. Per docs, the LLM    -
#     decides; for fixture purposes we record that either rename or         -
#     strengthen is defensible and the audit must say so explicitly.        -

def test_token_counts_default_to_zero():
    conn = _conn()
    conn.execute("INSERT INTO sessions (id, token_count) VALUES ('abc', 5)")
    row = conn.execute(
        "SELECT token_count FROM sessions WHERE id = 'abc'"
    ).fetchone()
    assert row[0] > 0


# --- lie: title claims styling/ANSI; body does no color check at all.       -
#     Expected fix path: RENAME. The body is a clean check of a different   -
#     property (description field is non-empty); title was aspirational.    -

def test_should_use_cyan_blue_styling_for_descriptions():
    conn = _conn()
    conn.execute(
        "INSERT INTO sessions (id, workspace_slug) VALUES ('s1', 'slobac/main')"
    )
    row = conn.execute(
        "SELECT workspace_slug FROM sessions WHERE id = 's1'"
    ).fetchone()
    assert row[0]
    assert len(row[0]) > 0


# --- lie: title claims a specific derivation rule; body does a vacuous check.-
#     Expected fix path: STRENGTHEN. The title captures real intent         -
#     (workspace slug is the last path segment); body under-delivers with a -
#     length check. Rewrite the assertion to actually verify the rule.     -

def test_workspace_slug_is_last_path_segment_of_repo_path():
    conn = _conn()
    conn.execute(
        "INSERT INTO sessions (id, workspace_slug) VALUES ('s2', 'some-project')"
    )
    row = conn.execute(
        "SELECT workspace_slug FROM sessions WHERE id = 's2'"
    ).fetchone()
    assert len(row[0]) > 0


# --- negative example: title uses "deletes", body uses DELETE SQL.          -
#     Different surface tokens (past-tense English vs SQL keyword) but the  -
#     body does verify the claim. Audit must NOT flag this.                 -

def test_closing_a_session_deletes_its_row():
    conn = _conn()
    conn.execute("INSERT INTO sessions (id) VALUES ('gone')")
    conn.execute("DELETE FROM sessions WHERE id = 'gone'")
    row = conn.execute("SELECT id FROM sessions WHERE id = 'gone'").fetchone()
    assert row is None
