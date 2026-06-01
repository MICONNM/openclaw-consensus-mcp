# Maintainer Workflow

## Triage

1. Label new issues as bug, enhancement, documentation, or security-sensitive.
2. Reproduce bugs against the latest release.
3. Ask for endpoint, client, and version details without requesting active API keys.

## Review

Pull requests should include tests for changed behavior and note any impact on:

- MCP tool schemas,
- endpoint requests and responses,
- secret handling,
- packaging,
- registry metadata.

## Release

1. Review the changelog.
2. Run `python -m pytest -q`.
3. Run `python -m build`.
4. Verify that `pyproject.toml`, `server.json`, README installation instructions, and the PyPI version agree.
5. Publish to PyPI.
6. Publish or refresh the MCP Registry entry after the matching PyPI version exists.

## Security

Treat API keys, endpoint URLs for private deployments, and user prompts as sensitive. Never log keys. Avoid adding network-backed tests that require real credentials to the default CI workflow.
