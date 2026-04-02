---
name: mcporter
name_en: mcporter
description: "管理和调用 MCP 服务器与工具。使用 mcporter CLI 直接列出、配置、认证和调用 MCP 服务器/工具，支持 HTTP 或 stdio 方式，包括临时服务器、配置编辑和 CLI/type 生成。"
description_en: "MCP server and tool management skill. Use mcporter CLI to list, configure, authenticate, and call MCP servers/tools directly. Supports HTTP and stdio modes, including ad-hoc servers, config editing, and CLI/type generation."
version: 1.0
author: 度量衡智库
author_en: Duliangheng Think Tank
category: tools
category_en: Developer Tools
---

# mcporter

Use `mcporter` to work with MCP servers directly.

Quick start
- `mcporter list`
- `mcporter list <server> --schema`
- `mcporter call <server.tool> key=value`

Call tools
- Selector: `mcporter call linear.list_issues team=ENG limit:5`
- Function syntax: `mcporter call "linear.create_issue(title: \"Bug\")"`
- Full URL: `mcporter call https://api.example.com/mcp.fetch url:https://example.com`
- Stdio: `mcporter call --stdio "bun run ./server.ts" scrape url=https://example.com`
- JSON payload: `mcporter call <server.tool> --args '{"limit":5}'`

Auth + config
- OAuth: `mcporter auth <server | url> [--reset]`
- Config: `mcporter config list|get|add|remove|import|login|logout`

Daemon
- `mcporter daemon start|status|stop|restart`

Codegen
- CLI: `mcporter generate-cli --server <name>` or `--command <url>`
- Inspect: `mcporter inspect-cli <path> [--json]`
- TS: `mcporter emit-ts <server> --mode client|types`

Notes
- Config default: `./config/mcporter.json` (override with `--config`).
- Prefer `--output json` for machine-readable results.
