# Submission Kit — OpenClaw Consensus MCP

Everything you need to copy/paste to land on the **MCP Registry** and
**awesome-mcp-servers**. ~5 minutes total.

---

## 0. Pre-flight: push the code to GitHub

Create a public repo named `openclaw-consensus-mcp` under your account
(`yanmiayn`), then from this folder:

```bash
git init -b main
git add .
git commit -m "feat: initial OpenClaw Consensus MCP server"
git remote add origin https://github.com/yanmiayn/openclaw-consensus-mcp.git
git push -u origin main
```

---

## 1. Publish to PyPI

```bash
# build
uv build

# (one-time) create a PyPI account: https://pypi.org/account/register/
# then publish
uv publish
# uv will prompt for your PyPI token; or set UV_PUBLISH_TOKEN
```

Verify: <https://pypi.org/project/openclaw-consensus-mcp/>

---

## 2. Publish to the official MCP Registry

### 2a. Install the publisher CLI

macOS / Linux:

```bash
curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/').tar.gz" \
  | tar xz mcp-publisher && sudo mv mcp-publisher /usr/local/bin/
```

Windows (PowerShell):

```powershell
$arch = if ([System.Runtime.InteropServices.RuntimeInformation]::ProcessArchitecture -eq "Arm64") { "arm64" } else { "amd64" }
Invoke-WebRequest -Uri "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_windows_$arch.tar.gz" -OutFile "mcp-publisher.tar.gz"
tar xf mcp-publisher.tar.gz mcp-publisher.exe
# Move mcp-publisher.exe somewhere in your PATH.
```

### 2b. Auth + publish

```bash
mcp-publisher login github     # opens https://github.com/login/device
mcp-publisher publish          # reads server.json from cwd
```

The `server.json` file in this repo is already correct. Verification works
because `README.md` contains the line:

```html
<!-- mcp-name: io.github.yanmiayn/openclaw-consensus -->
```

…and that string is also embedded in the PyPI package description (PyPI uses
the README), which is what the registry checks.

Verify after publishing:

```bash
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=openclaw-consensus"
```

---

## 3. PR to `punkpeye/awesome-mcp-servers`

Repo: <https://github.com/punkpeye/awesome-mcp-servers>

### Branch name

```
add-openclaw-consensus
```

### Section to edit

The list is grouped by category. OpenClaw belongs in either:

- **🔗 Aggregators** — "Servers for accessing many apps and tools through a single MCP server." (best fit; OpenClaw aggregates 9 LLMs)

Insert the line in **alphabetical order** within the section.

### Exact line to add

```markdown
- [yanmiayn/openclaw-consensus-mcp](https://github.com/yanmiayn/openclaw-consensus-mcp) 🐍 ☁️ - 9-LLM consensus answers, disagreement scoring, and cheapest-route recommendations to fight hallucinations. Built by a 16yo Korean solo dev.
```

(emoji legend per the repo: 🐍 = Python, ☁️ = cloud service)

### PR title

```
Add openclaw-consensus 🤖🤖🤖
```

(The `🤖🤖🤖` suffix opts the PR into the maintainer's expedited automated-agent merge lane, per CONTRIBUTING.md.)

### PR body

```markdown
## What

Adds **OpenClaw Consensus** to the Aggregators section.

OpenClaw is a 9-LLM consensus API exposed as an MCP server. Tools:

1. `consensus(prompt, mode)` — consensus answer with confidence
2. `disagreement_score(prompt)` — hallucination warning signal
3. `cheapest_route(prompt, target_quality)` — cost-optimised model picker

## Why

Single LLMs hallucinate confidently. Nine models rarely hallucinate the same thing — disagreement is a calibrated, cheap pre-flight check.

## Links

- Repo: https://github.com/yanmiayn/openclaw-consensus-mcp
- PyPI: https://pypi.org/project/openclaw-consensus-mcp/
- MCP Registry: `io.github.yanmiayn/openclaw-consensus`
- RapidAPI: https://rapidapi.com/yanmiayn/api/openclaw-consensus

Built solo by a 16-year-old Korean indie dev.
```

### How to actually file it (UI, ~2 min)

1. Visit <https://github.com/punkpeye/awesome-mcp-servers> and click **Fork**.
2. In your fork, open `README.md`, click the pencil icon.
3. Paste the line above into the **🔗 Aggregators** section, alphabetically.
4. Commit to a new branch `add-openclaw-consensus`.
5. Click **Compare & pull request**, paste the title and body above, submit.

---

## 4. (Optional) PR to `modelcontextprotocol/servers` "Community Servers"

Note: as of late-2025 the official `modelcontextprotocol/servers` repo has
been migrating community listings into the **MCP Registry** (Step 2). Once
your registry publish succeeds, the registry is the canonical listing — a PR
to the `servers` repo's README is no longer required. Skip unless you see an
explicit "community servers" section still accepting new entries.

---

## 5. Hetzner backend (Phase 2 — optional)

A systemd unit for hosting the MCP server over SSE on the existing
`openclaw-gateway` box. Not required for stdio-based clients (Claude Desktop,
Claude Code) — file under "do this only if you want a hosted variant".

```ini
# /etc/systemd/system/openclaw-mcp.service
[Unit]
Description=OpenClaw Consensus MCP (SSE)
After=network-online.target

[Service]
EnvironmentFile=/etc/openclaw.env
ExecStart=/usr/local/bin/openclaw-consensus
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable --now openclaw-mcp
journalctl -u openclaw-mcp -f
```

For SSE transport you would change `mcp.run(transport="stdio")` to
`mcp.run(transport="sse", host="0.0.0.0", port=19001)` in `server.py` —
intentionally left as a Phase-2 toggle.
