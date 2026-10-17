
from langchain_core.tools import StructuredTool



def convert_mcp_tool(mcp_tool, call_tool):
    """Convert one MCP tool into a LangChain tool."""

    async def execute_tool(**kwargs):
        result = await call_tool(mcp_tool.name, kwargs)

        return "\n".join(
            item.text
            for item in result.content
            if item.type == "text"
        )

    return StructuredTool.from_function(
        coroutine=execute_tool,
        name=mcp_tool.name,
        description=mcp_tool.description or "",
        args_schema=mcp_tool.inputSchema,
    )
