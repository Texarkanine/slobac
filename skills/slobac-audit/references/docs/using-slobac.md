# Running the SLOBAC Audit

## Install

Install the [txrk9-agent-plugins](https://github.com/Texarkanine/txrk9-agent-plugins) Plugin Marketplace into your harness of choice.

Then, install the `slobac` plugin from that marketplace.

This will give your harness access to the `/slobac-audit` [Agent Skill](https://agentskills.io).

## Scope

The audit is intended to be **read-only**: it reports findings; it does not modify test code. A report is created that you can feed into your chosen remediation process.

You may run the audit against a single test, a single test suite, a directory tree, or multiple trees of tests within your repository - it will ask you to choose.

You may run the audit looking for a subset of the [taxonomy](./taxonomy/README.md) of test smells. If you don't specify, it will ask you to choose. You can use `all` to search for all smells.

    /slobac-audit src/test/java/ all smells

## Context window

**For best results, run SLOBAC with the most-capable model and largest context window available.** 

* In Cursor, enable MAX mode and pick a heavyweight, frontier model.
* In Claude Code, use Opus with the 1M context window.

Larger context means fewer batches, richer cross-suite analysis, and better recall on redundancy detection. SLOBAC works at 200K context but shards more aggressively, trading recall on cross-suite smells for safety.

Pass your context window size in the invocation to skip the one-time question the orchestrator asks when it encounters a large suite without a stated budget.

    /slobac-audit src/test/java/ all smells - 1M context window
