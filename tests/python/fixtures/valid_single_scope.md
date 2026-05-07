# Naming Lies

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `naming-lies` | Medium | per-test | [Understandable](../principles/test-qualities.md#understandable), [Well-named](../principles/test-qualities.md#well-named) |

## Summary

Trimmed fixture for parse-entry testing. Real entries carry many more
sections; the parser only reads the header table at the top.
