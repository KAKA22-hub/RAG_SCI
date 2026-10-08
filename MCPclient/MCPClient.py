from fastmcp import Client
import asyncio
from fastmcp.client.transports import StreamableHttpTransport


MCP_SERVER_URL = "http://localhost:9000/mcp"
def call_mcp_tool(tool_name: str,  token, **kwargs):
    async def async_call_tool():
        kwargs["user_token"] = token
        async with Client(MCP_SERVER_URL) as client:
            result = await client.call_tool(tool_name, kwargs)
            return result.data if hasattr(result, "data") else str(result)
    return asyncio.run(async_call_tool())