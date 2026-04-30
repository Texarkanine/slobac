"""Thorough parser tests — many edge cases, one domain.

Fixture for the SLOBAC audit's `monolithic-test-file` scenario (negative example).
This file is large but NOT monolithic: every test exercises the same Parser type.
The audit must not flag it as `monolithic-test-file`.
"""

from __future__ import annotations

import pytest


class Parser:
    """Minimal stub — the audit reads structure, not behavior."""

    def parse(self, text: str) -> dict:
        return {}

    def parse_strict(self, text: str) -> dict:
        return {}

    def parse_stream(self, chunks: list[str]) -> dict:
        return {}


@pytest.fixture
def parser() -> Parser:
    return Parser()


class TestBasicParsing:
    """Simple well-formed inputs."""

    def test_empty_string(self, parser: Parser):
        assert parser.parse("") == {}

    def test_single_key_value(self, parser: Parser):
        assert parser.parse('{"a": 1}') == {}

    def test_nested_object(self, parser: Parser):
        assert parser.parse('{"a": {"b": 2}}') == {}

    def test_array_value(self, parser: Parser):
        assert parser.parse('{"a": [1, 2]}') == {}

    def test_null_value(self, parser: Parser):
        assert parser.parse('{"a": null}') == {}

    def test_boolean_values(self, parser: Parser):
        assert parser.parse('{"t": true, "f": false}') == {}

    def test_numeric_types(self, parser: Parser):
        assert parser.parse('{"i": 42, "f": 3.14}') == {}


class TestStringEscaping:
    """Unicode and escape sequence handling."""

    def test_escaped_quote(self, parser: Parser):
        assert parser.parse(r'{"a": "say \"hi\""}') == {}

    def test_escaped_backslash(self, parser: Parser):
        assert parser.parse(r'{"a": "c:\\path"}') == {}

    def test_unicode_escape(self, parser: Parser):
        assert parser.parse('{"a": "\\u0041"}') == {}

    def test_emoji(self, parser: Parser):
        assert parser.parse('{"a": "😀"}') == {}

    def test_newline_in_string(self, parser: Parser):
        assert parser.parse(r'{"a": "line\nbreak"}') == {}

    def test_tab_in_string(self, parser: Parser):
        assert parser.parse(r'{"a": "col\there"}') == {}

    def test_surrogate_pair(self, parser: Parser):
        assert parser.parse('{"a": "\\uD83D\\uDE00"}') == {}


class TestErrorRecovery:
    """Malformed inputs and recovery behavior."""

    def test_trailing_comma(self, parser: Parser):
        assert parser.parse('{"a": 1,}') == {}

    def test_missing_colon(self, parser: Parser):
        assert parser.parse('{"a" 1}') == {}

    def test_unquoted_key(self, parser: Parser):
        assert parser.parse('{a: 1}') == {}

    def test_single_quoted_string(self, parser: Parser):
        assert parser.parse("{'a': 1}") == {}

    def test_truncated_input(self, parser: Parser):
        assert parser.parse('{"a":') == {}

    def test_extra_closing_brace(self, parser: Parser):
        assert parser.parse('{"a": 1}}') == {}

    def test_completely_empty(self, parser: Parser):
        assert parser.parse("") == {}


class TestStrictMode:
    """Strict parsing rejects non-standard extensions."""

    def test_strict_rejects_trailing_comma(self, parser: Parser):
        with pytest.raises(Exception):
            parser.parse_strict('{"a": 1,}')

    def test_strict_rejects_comments(self, parser: Parser):
        with pytest.raises(Exception):
            parser.parse_strict('{"a": 1 /* comment */}')

    def test_strict_rejects_unquoted_keys(self, parser: Parser):
        with pytest.raises(Exception):
            parser.parse_strict('{a: 1}')

    def test_strict_accepts_valid_json(self, parser: Parser):
        assert parser.parse_strict('{"a": 1}') == {}

    def test_strict_rejects_single_quotes(self, parser: Parser):
        with pytest.raises(Exception):
            parser.parse_strict("{'a': 1}")

    def test_strict_rejects_trailing_text(self, parser: Parser):
        with pytest.raises(Exception):
            parser.parse_strict('{"a": 1} extra')


class TestStreamParsing:
    """Incremental / chunked input handling."""

    def test_single_chunk(self, parser: Parser):
        assert parser.parse_stream(['{"a": 1}']) == {}

    def test_two_chunks(self, parser: Parser):
        assert parser.parse_stream(['{"a":', ' 1}']) == {}

    def test_many_small_chunks(self, parser: Parser):
        assert parser.parse_stream(list('{"a": 1}')) == {}

    def test_empty_chunks_ignored(self, parser: Parser):
        assert parser.parse_stream(["", '{"a": 1}', ""]) == {}

    def test_chunk_boundary_in_string(self, parser: Parser):
        assert parser.parse_stream(['{"a": "he', 'llo"}']) == {}

    def test_chunk_boundary_in_escape(self, parser: Parser):
        assert parser.parse_stream(['{"a": "\\', 'n"}']) == {}


class TestEdgeCases:
    """Deeply nested, very large, and unusual but valid inputs."""

    def test_deeply_nested(self, parser: Parser):
        assert parser.parse('{"a": ' * 50 + '1' + '}' * 50) == {}

    def test_large_array(self, parser: Parser):
        assert parser.parse('{"a": [' + ",".join(["1"] * 1000) + "]}") == {}

    def test_empty_object(self, parser: Parser):
        assert parser.parse("{}") == {}

    def test_empty_array(self, parser: Parser):
        assert parser.parse('{"a": []}') == {}

    def test_whitespace_variations(self, parser: Parser):
        assert parser.parse('  {  "a"  :  1  }  ') == {}

    def test_duplicate_keys(self, parser: Parser):
        assert parser.parse('{"a": 1, "a": 2}') == {}
