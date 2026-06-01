# Publication Checklist

This repository is public at <https://github.com/MICONNM/openclaw-consensus-mcp>.

## Release

1. Confirm `CHANGELOG.md` documents the release.
2. Run `python -m pytest -q`.
3. Run `python -m build`.
4. Confirm the version in `pyproject.toml` is not already on PyPI.
5. Publish with `uv publish`.
6. Verify <https://pypi.org/project/openclaw-consensus-mcp/>.

## MCP Registry

The registry metadata lives in `server.json`.

Before publishing:

1. Confirm the package version in `server.json` exists on PyPI.
2. Confirm the repository URL and MCP name use the `MICONNM` GitHub namespace.
3. Run `mcp-publisher login github`.
4. Run `mcp-publisher publish`.

Verify:

```bash
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=openclaw-consensus"
```

## Listing Requests

When requesting inclusion in a community list:

1. Read the target repository's current contribution guide.
2. Use the target repository's current category and formatting rules.
3. Describe only capabilities verified in this repository.
4. Link to this repository, PyPI, and the MCP Registry entry when available.

Do not claim download counts, registry approval, or external adoption without checking the current source first.
