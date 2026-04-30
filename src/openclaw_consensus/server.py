"""OpenClaw Consensus MCP server entrypoint.

Exposes three tools to MCP clients (Claude Desktop, Claude Code, etc.):

  - ``consensus``: 9-LLM consensus answer with confidence + disagreement
  - ``disagreement_score``: how much the 9 models disagree (hallucination signal)
  - ``cheapest_route``: cheapest model combo that meets a quality threshold

Run with::

    python -m openclaw_consensus.server
    # or, after `pip install openclaw-consensus-mcp`:
    openclaw-consensus
"""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from .client import OpenClawClient, OpenClawError

mcp = FastMCP("openclaw-consensus")
_client = OpenClawClient()


_VALID_MODES = {"deep", "balanced", "fast"}


@mcp.tool()
async def consensus(prompt: str, mode: str = "balanced") -> dict[str, Any]:
    """Get a 9-LLM consensus answer.

    Args:
        prompt: The user question or instruction.
        mode: ``deep`` (9 models), ``balanced`` (5), or ``fast`` (3).

    Returns:
        A dict with ``answer``, ``confidence`` (0..1), ``models_used`` (list),
        and ``disagreement`` (0..1, higher = riskier hallucination signal).
    """
    if mode not in _VALID_MODES:
        return {"error": f"mode must be one of {sorted(_VALID_MODES)}"}
    try:
        return await _client.consensus(prompt, mode=mode)
    except OpenClawError as e:
        return {"error": str(e)}


@mcp.tool()
async def disagreement_score(prompt: str) -> dict[str, Any]:
    """Score how much the 9 models disagree on a prompt (0..1).

    A high score is a useful hallucination warning: when frontier models
    disagree, single-model answers are more likely to be wrong.

    Returns:
        ``{"score": float, "per_model": {model: answer_summary}}``.
    """
    try:
        return await _client.disagreement(prompt)
    except OpenClawError as e:
        return {"error": str(e)}


@mcp.tool()
async def cheapest_route(
    prompt: str, target_quality: float = 0.85
) -> dict[str, Any]:
    """Recommend the cheapest model combination that meets a quality bar.

    Args:
        prompt: The user prompt to route.
        target_quality: Minimum acceptable quality, 0..1. Default 0.85.

    Returns:
        ``{"models": [...], "estimated_cost_usd": float, "estimated_quality": float}``.
    """
    if not 0.0 <= target_quality <= 1.0:
        return {"error": "target_quality must be between 0 and 1"}
    try:
        return await _client.cheapest_route(prompt, target_quality=target_quality)
    except OpenClawError as e:
        return {"error": str(e)}


def main() -> None:
    """Entrypoint used by the ``openclaw-consensus`` console script."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
