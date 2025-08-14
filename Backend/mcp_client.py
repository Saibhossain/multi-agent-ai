import asyncio, os
from typing import Optional, Any, Dict
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv()

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def start(self) -> None:
        script = os.getenv("MCP_SERVER_SCRIPT","../mcp_server/server.py")
        command = "python" if script.endswith(".py") else "node"
        server_params = StdioServerParameters(command=command, args=[script], env=None)
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

    async def stop(self) -> None:
        await self.exit_stack.aclose()

    async def call(self, tool: str, args: Dict[str, Any]) -> Any:
        if not self.session:
            raise RuntimeError("MCP session not started")
        result = await self.session.call_tool(tool, args)
        parts = result.content or []
        for part in parts:
            if part.get("type") == "text":
                return part.get("text")
            if part.get("type") == "json":
                return part.get("json")
        return parts