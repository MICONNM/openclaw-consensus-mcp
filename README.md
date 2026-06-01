# OpenClaw Consensus MCP

[![CI](https://github.com/MICONNM/openclaw-consensus-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/MICONNM/openclaw-consensus-mcp/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/openclaw-consensus-mcp.svg)](https://pypi.org/project/openclaw-consensus-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Multi-model consensus inside MCP clients: compare answers, surface disagreement, and escalate only when needed.

OpenClaw Consensus MCP wraps the OpenClaw Consensus API as three Model Context Protocol tools. It is designed for workflows where a maintainer wants a second opinion before accepting a risky answer, review summary, or routing decision.

<!-- mcp-name: io.github.MICONNM/openclaw-consensus-mcp -->

## What it does

OpenClaw runs the same prompt across multiple models, then returns:

- a **consensus answer** with confidence and model response metadata,
- a **disagreement heuristic** derived from the deep consensus response, and
- a **cheapest route** recommendation that tries smaller model sets before escalating.

This MCP server exposes those three capabilities as tools so Claude Desktop / Claude Code can call them mid-conversation.

## Why consensus?

A single model can produce a confident but incorrect answer. Comparing multiple responses does not prove correctness, but disagreement is a useful signal that a maintainer should review the output more carefully.

## Install

```bash
pip install openclaw-consensus-mcp
# or
uv pip install openclaw-consensus-mcp
```

You also need a RapidAPI key for the OpenClaw Consensus API:
<https://rapidapi.com/yanmiayn/api/openclaw-consensus>

Set it in your environment:

```bash
export RAPIDAPI_KEY="your-rapidapi-key"
```

## Claude Desktop config

Add to `~/.claude/claude_desktop_config.json` (macOS/Linux) or
`%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "openclaw-consensus": {
      "command": "openclaw-consensus",
      "env": {
        "RAPIDAPI_KEY": "your-rapidapi-key"
      }
    }
  }
}
```

For Claude Code:

```bash
claude mcp add openclaw-consensus -- openclaw-consensus
```

## Tools

### `consensus(prompt, mode="balanced")`

Get a 9-LLM consensus answer.

- **prompt** *(string)* — the question.
- **mode** *(string, default `balanced`)* — `deep` (9 models), `balanced` (5), or `fast` (3).

**Returns**

```json
{
  "answer": "string",
  "confidence": 0.0,
  "models_responded": 5,
  "votes": []
}
```

### `disagreement_score(prompt)`

How much the deep consensus response disagrees on a prompt.

**Returns**

```json
{
  "disagreement": 0.0,
  "confidence": 1.0,
  "models_responded": 9,
  "votes": []
}
```

### `cheapest_route(prompt, target_quality=0.85)`

Try `fast`, `balanced`, and `deep` modes in order until the confidence threshold is met.

**Returns**

```json
{
  "selected_mode": "balanced",
  "models_used": 5,
  "confidence": 0.9,
  "answer": "string"
}
```

## Local development

```bash
git clone https://github.com/MICONNM/openclaw-consensus-mcp
cd openclaw-consensus-mcp
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
pytest
```

Smoke-test the server with the official MCP Inspector:

```bash
npx @modelcontextprotocol/inspector openclaw-consensus
```

## Publish

```bash
uv build
uv publish      # to PyPI
mcp-publisher publish   # to the official MCP Registry
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow and [docs/maintainer-workflow.md](docs/maintainer-workflow.md) for triage, review, security, and release responsibilities.

## Limitations

- Consensus is a review aid, not a correctness guarantee.
- Network-backed tools require a configured OpenClaw endpoint and may incur provider charges.
- Do not send secrets, private source code, or personal data unless your endpoint policy explicitly allows it.

## Security

Please report vulnerabilities privately using the process in [SECURITY.md](SECURITY.md).

## License

MIT — see [LICENSE](LICENSE).
