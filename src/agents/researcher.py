
import sys
from pathlib import Path

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from src.adapters.mcp_to_langchain import convert_mcp_tool


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVER_PATH = PROJECT_ROOT / "src" / "mcp_server" / "server.py"


async def research(question: str) -> str:
    """Research a question using the MCP document tools."""

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

            # Bridge MCP tool calls to the client session
            async def call_tool(name, arguments):
                return await session.call_tool(
                    name,
                    arguments=arguments,
                )

            # Convert MCP tools into LangChain tools
            tools = [
                convert_mcp_tool(tool, call_tool)
                for tool in mcp_tools
            ]

            # Create the LLM
            llm = ChatGroq(model="openai/gpt-oss-120b")

            # Create a tool-using LangChain agent
            agent = create_agent(
                model=llm,
                tools=tools,
                system_prompt=(
                    "You are a research assistant. Use the available "
                    "document tools to find relevant information. "
                    "Base your answer on retrieved documents and "
                    "state when the documents do not contain enough "
                    "information."
                ),
            )

            # Run the agent
            result = await agent.ainvoke(
                {
                    "messages": [
                        {"role": "user", "content": question}
                    ]
                }
            )

            return result["messages"][-1].content
