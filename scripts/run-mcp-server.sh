#!/bin/bash
# Context-aware MCP server launcher.
# Works from both the host (direct run.sh) and inside the devcontainer (sudo privileged wrapper).
# Usage: run-mcp-server.sh <server-name>

set -euo pipefail

SERVER_NAME="${1:?Usage: $(basename "$0") <server-name>}"
SHARED_STORE="${SHARED_STORE:-/shared/store}"

if [[ -n "${WORKSPACEROOT:-}" ]]; then
	# Inside devcontainer: WORKSPACEROOT=/workspace is set in containerEnv.
	# Secrets are root-owned; use the privileged wrapper baked into the image.
	# Requires: agent ALL=(root) NOPASSWD:SETENV: /opt/devcontainer/run-mcp-privileged.sh
	# Rebuild the devcontainer image if this fails.
	exec sudo /opt/devcontainer/run-mcp-privileged.sh "${SHARED_STORE}/${SERVER_NAME}"
fi

# On host: run directly from the shared store.
# API keys must be exported in the environment (e.g. via direnv or shell .env sourcing).
exec "${SHARED_STORE}/${SERVER_NAME}/run.sh"
