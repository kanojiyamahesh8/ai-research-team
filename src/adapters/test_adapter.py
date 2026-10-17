
import asyncio
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from src.adapters.mcp_to_langchain import convert_mcp_tool


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVER_PATH = PROJECT_ROOT / "src" / "mcp_server" / "server.py"


async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        cwd=str(PROJECT_ROOT),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Discover MCP tools
            mcp_tools = (await session.list_tools()).tools

            # Inspect the MCP input schema
            search_mcp_tool = next(
                tool for tool in mcp_tools
                if tool.name == "search_documents"
            )

            # print("MCP schema type:", type(search_mcp_tool.inputSchema))
            # print("MCP schema:", search_mcp_tool.inputSchema)

            # Provide an async function for the adapter to call
            async def call_tool(name, arguments):
                return await session.call_tool(
                    name,
                    arguments=arguments,
                )

            # Convert the MCP tool into a LangChain tool
            langchain_tool = convert_mcp_tool(
                search_mcp_tool,
                call_tool,
            )

            # Inspect the schema LangChain uses
            # print(
            #     "\nLangChain args_schema type:",
            #     type(langchain_tool.args_schema),
            # )
            # print("LangChain args:", langchain_tool.args)

            # Test the LangChain tool
            result = await langchain_tool.ainvoke(
                {"query": "MCP protocol"}
            )

            
            # Test the second MCP tool: get_document
            document_mcp_tool = next(
                tool for tool in mcp_tools
                if tool.name == "get_document"
            )

            document_langchain_tool = convert_mcp_tool(
                document_mcp_tool,
                call_tool,
            )

            document_result = await document_langchain_tool.ainvoke(
                {"document_id": "doc1"}
            )

            print("\nSecond LangChain tool:", document_langchain_tool.name)
            print("Document result:")
            print(document_result)


            print("\nLangChain tool name:", langchain_tool.name)
            print("Result:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
