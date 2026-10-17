
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Locate the project root and our MCP server
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVER_PATH = PROJECT_ROOT / "src" / "mcp_server" / "server.py"


async def main():
    # Start our MCP server using the current Python environment
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        cwd=str(PROJECT_ROOT),
    )

    # Establish communication over stdio
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Initialize the MCP session
            await session.initialize()
            print("Connected to our MCP server!\n")

            # Discover available tools
            tools_result = await session.list_tools()

            print("Available tools:")
            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description}")

            # Call the search tool
            print("\nSearching documents...")
            search_result = await session.call_tool(
                "search_documents",
                arguments={"query": "MCP protocol"},
            )

            print("\nSearch result:")
            for item in search_result.content:
                if item.type == "text":
                    print(item.text)

            # Retrieve a specific document
            print("\nRetrieving doc1...")
            document_result = await session.call_tool(
                "get_document",
                arguments={"document_id": "doc1"},
            )

            print("\nDocument result:")
            for item in document_result.content:
                if item.type == "text":
                    print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
