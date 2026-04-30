# OpenClaw Consensus MCP

> 9-LLM consensus inside Claude — a hallucination guardrail you can call as a tool.

Built by **yanmiayn** — 16yo solo dev from Korea, building 9-LLM consensus to fight hallucinations.

<!-- mcp-name: io.github.MICONNM/openclaw-consensus-mcp -->

## What it does

OpenClaw runs the same prompt across 9 frontier LLMs (Claude, GPT, Gemini, Llama, Mistral, etc.), then returns:

- a **consensus answer** (with confidence + which models contributed),
- a **disagreement score** (high = your single LLM is probably about to hallucinate), and
- a **cheapest route** (pick the smallest model combo that still hits your quality bar).

This MCP server exposes those three capabilities as tools so Claude Desktop / Claude Code can call them mid-conversation.

## Why consensus?

A single LLM can confidently make things up. Nine models rarely make up the *same* thing. When 9 models agree, you can trust the answer; when they fan out, you have a cheap, calibrated hallucination signal — before the user sees the wrong answer.

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
  "models_used": ["claude-opus-4.7", "gpt-5.1", "..."],
  "disagreement": 0.0
}
```

### `disagreement_score(prompt)`

How much the 9 models disagree on a prompt — a hallucination warning signal.

**Returns**

```json
{
  "score": 0.0,
  "per_model": { "model-id": "answer summary" }
}
```

### `cheapest_route(prompt, target_quality=0.85)`

Cheapest model combo that meets a quality threshold (0..1).

**Returns**

```json
{
  "models": ["..."],
  "estimated_cost_usd": 0.0,
  "estimated_quality": 0.0
}
```

## Local development

```bash
git clone https://github.com/yanmiayn/openclaw-consensus-mcp
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

## License

MIT — see [LICENSE](LICENSE).
