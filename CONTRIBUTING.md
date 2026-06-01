# Contributing

Thanks for helping improve OpenClaw Consensus MCP.

## Development Setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest -q
```

On Windows PowerShell, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Pull Requests

1. Open an issue first for behavior changes or new tools.
2. Keep changes focused and add tests for changed behavior.
3. Run `python -m pytest -q` and `python -m build` before opening a pull request.
4. Describe user-visible behavior, security impact, and release-note needs.

## Reporting Bugs

Use the bug report issue template for reproducible defects. For vulnerabilities, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.
