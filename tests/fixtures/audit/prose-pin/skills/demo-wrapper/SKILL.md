---
name: demo-wrapper
description: Thin agent-facing wrapper around the demo CLI. Prefer the on-path shim; do not invoke the Python module directly.
---

# Demo Wrapper

Use the on-path `demo` command for all agent actions.

## Flags

When inspecting a run, pass `--detail raw` to dump the unprocessed payload.
For machine-readable output, pass `--format json` after selecting the detail level.
