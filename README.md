# MCP-Research-Server
A production-grade MCP server for research automation, Obsidian integration, and web search

# 🧠 MCP Research Server (The Sixth Server)

A Model Context Protocol (MCP) server that connects Claude to your local files and the web.

## 🚀 Setup
1. `pip install -r requirements.txt`
2. Update your `claude_desktop_config.json` with the absolute path to `server.py`.
3. Set your `WORKSPACE` environment variable to your Obsidian or Notes folder.

## 🛠️ Features
- **FTS5 Search**: Native SQLite full-text search.
- **Async Execution**: Non-blocking tool calls.
- **Dockerized**: Ready for containerized deployment.
