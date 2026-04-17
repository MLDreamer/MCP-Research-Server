import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
import handlers
from database import init_db

app = Server("research-server")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="web_search",
            description="Search the web. Best used BEFORE saving notes.",
            inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
        ),
        types.Tool(
            name="search_notes",
            description="Search your local vault. Use for 'What do I know about...'",
            inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    tool_map = {"web_search": handlers.handle_web_search, "search_notes": handlers.handle_search_notes}
    handler = tool_map.get(name)
    try:
        result = await handler(arguments)
        return [types.TextContent(type="text", text=str(result))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    init_db(handlers.DB_PATH)
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
