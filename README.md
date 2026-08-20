# Selvage

AI-powered autonomous code implementation pipeline. Describe what you want — selvage implements, verifies, and reviews it.

## Quick Start

```bash
# Install
brew install runselvage/selvage/selvage

# Run in any git repo
cd my-project
selvage run "add retry logic to the HTTP client with exponential backoff"
```

That's it. Selvage auto-detects your project, picks the best available AI tools, implements the change, runs your tests, and lands the result on a local branch.

## How It Works

```
You describe → Implementer codes → Verification runs → Reviewer checks → Lands on branch
```

1. **You describe** what you want (CLI or MCP)
2. **Implementer** writes the code in an isolated worktree
3. **Verification** runs build + tests automatically
4. **Reviewer** (different AI model) checks for correctness
5. **Result** lands on a local branch for you to merge

## Install

### Homebrew (macOS/Linux)

```bash
brew install runselvage/selvage/selvage
```

### Direct download

```bash
# macOS Apple Silicon
curl -L https://github.com/runselvage/selvage/releases/latest/download/selvage-darwin-arm64.tar.gz | tar xz
sudo mv selvage /usr/local/bin/

# macOS Intel
curl -L https://github.com/runselvage/selvage/releases/latest/download/selvage-darwin-amd64.tar.gz | tar xz
sudo mv selvage /usr/local/bin/

# Linux x86_64
curl -L https://github.com/runselvage/selvage/releases/latest/download/selvage-linux-amd64.tar.gz | tar xz
sudo mv selvage /usr/local/bin/
```

### Go install

> **Note:** Not available yet. Use Homebrew or direct download.

## Requirements

- **Git** (local repo required)
- **One AI tool** on PATH: `kiro-cli`, `claude`, `opencode`, or `codex`

No GitHub account needed. No remote repo needed. Works fully local.

## Usage

### Run a task

```bash
# Describe what you want
selvage run "add input validation to the signup form"

# Work a GitHub issue (if GitHub is configured)
selvage run 42

# Run multiple issues as a batch plan
selvage plan run 100 101 102 103
```

### Check status

```bash
selvage status
```

### Approve and merge

```bash
# Review the changes
git diff main..selvage/<task-id>

# Approve (when human gate is enabled)
selvage approve <task-id>
```

## MCP Integration

Use selvage as an MCP tool server with Claude Desktop, Cursor, or any MCP-compatible client:

```json
{
  "mcpServers": {
    "selvage": {
      "command": "selvage",
      "args": ["mcp-server", "--repo", "/path/to/your/project"]
    }
  }
}
```

Available tools:
- `selvage_submit_task` — submit work
- `selvage_implement_spec` — submit a design spec for implementation
- `selvage_status` — check task status
- `selvage_get_evidence` — read task evidence and review results
- `selvage_record_review` — record a supplemental review

## Configuration

On first run, selvage auto-generates `.selvage/config.yaml` based on your project:

```yaml
version: 0.1.0
verification:
    checks:
        - name: build
          command: [go, build, ./...]
          timeout: 2m0s
        - name: test
          command: [go, test, ./...]
          timeout: 3m0s
```

Customize adapters, verification checks, and review policies as needed.

## Features

- **Worktree isolation** — changes are made in a separate git worktree, never touching your working directory
- **Automatic verification** — build and tests run after every implementation
- **Cross-model review** — a different AI model reviews the implementation for correctness
- **Plan execution** — batch multiple issues into a single aggregate branch
- **Drift replay** — handles rebasing when the base branch moves
- **MCP server** — integrate with any MCP-compatible AI client

## Links

- Website: [selvage.run](https://selvage.run)
- Documentation: [selvage.sh](https://selvage.sh)

## License

Proprietary. See [LICENSE](LICENSE) for details.
