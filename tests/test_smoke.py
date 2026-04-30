"""Smoke tests — no network calls, just verify imports and tool registration."""

from __future__ import annotations


def test_package_imports() -> None:
    import openclaw_consensus
    assert openclaw_consensus.__version__


def test_server_module_imports() -> None:
    from openclaw_consensus import server
    assert server.mcp is not None
    assert server.mcp.name == "openclaw-consensus"


def test_client_constructs_without_key() -> None:
    from openclaw_consensus.client import OpenClawClient
    c = OpenClawClient(api_key="")
    headers = c._headers()
    assert "X-RapidAPI-Host" in headers
    assert "X-RapidAPI-Key" not in headers


def test_client_includes_key_when_set() -> None:
    from openclaw_consensus.client import OpenClawClient
    c = OpenClawClient(api_key="test-key")
    assert c._headers()["X-RapidAPI-Key"] == "test-key"
