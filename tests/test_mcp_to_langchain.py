
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from src.adapters.mcp_to_langchain import convert_mcp_tool


@pytest.mark.asyncio
async def test_convert_mcp_tool_calls_mcp_and_returns_text():
    mcp_tool = SimpleNamespace(
        name="search_documents",
        description="Search local documents",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
            },
            "required": ["query"],
        },
    )

    mcp_result = SimpleNamespace(
        content=[
            SimpleNamespace(type="text", text="First result"),
            SimpleNamespace(type="image", text=None),
            SimpleNamespace(type="text", text="Second result"),
        ]
    )

    call_tool = AsyncMock(return_value=mcp_result)

    langchain_tool = convert_mcp_tool(mcp_tool, call_tool)

    result = await langchain_tool.ainvoke({"query": "MCP protocol"})

    call_tool.assert_awaited_once_with(
        "search_documents",
        {"query": "MCP protocol"},
    )
    assert result == "First result\nSecond result"
    assert langchain_tool.name == "search_documents"
    assert langchain_tool.description == "Search local documents"
