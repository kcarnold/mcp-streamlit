# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MCP-Streamlit is an interactive Streamlit app for chatting with LLMs via Model Context Protocol (MCP). It connects to various MCP servers and provides a chat interface with tool integration.

## Core Architecture

- **Entry Point**: `app/streamlit_app.py` - Main Streamlit application that orchestrates server selection and UI
- **MCP Client**: `app/client.py` - Async context manager for connecting to MCP servers via stdio
- **UI Layer**: `app/ui.py` - Chat interface and agent loop for handling LLM conversations with tool calls
- **Server Configuration**: `app/servers/servers_list.py` - Predefined MCP server configurations

The application follows an async pattern where:
1. User selects an MCP server from `servers_list.py`
2. `MCPClient` connects via stdio and retrieves available tools
3. Tools are stored in Streamlit session state and displayed in sidebar
4. Chat UI handles user input, LLM responses, and tool execution through an agent loop

## Development Commands

**Run the application:**
```bash
uv run streamlit run app/streamlit_app.py
```

## Environment Configuration

Copy `.env.example` to `.env` and set required variables:
- `GITHUB_PERSONAL_ACCESS_TOKEN` - Required for GitHub MCP server
- OpenAI/Azure OpenAI credentials for LLM access

## Key Implementation Details

- **Tool Integration**: Tools from MCP servers are wrapped as callables and converted to OpenAI function schemas
- **Session Management**: Streamlit session state manages MCP tools, conversation history, and server parameters
- **Async Context**: MCP connections use async context managers for proper resource cleanup
- **Agent Loop**: `ui.py:agent_loop()` handles the conversation flow including tool calls and responses

## Available MCP Servers

- **weather**: Local Python weather server
- **mcp_server_fetch**: Fetch server via pip package
- **github**: GitHub API server requiring personal access token