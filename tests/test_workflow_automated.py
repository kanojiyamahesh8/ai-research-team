
from unittest.mock import AsyncMock, patch

import pytest

from src.agents.workflow import build_workflow


@pytest.mark.asyncio
async def test_workflow_generates_report_when_review_accepts():
    with (
        patch(
            "src.agents.workflow.research",
            new_callable=AsyncMock,
            return_value="Research findings",
        ) as mock_research,
        patch(
            "src.agents.workflow.review_research",
            new_callable=AsyncMock,
            return_value="RECOMMENDATION: ACCEPT",
        ) as mock_review,
        patch(
            "src.agents.workflow.write_report",
            new_callable=AsyncMock,
            return_value="# Final Report",
        ) as mock_writer,
    ):
        workflow = build_workflow()

        result = await workflow.ainvoke({
            "question": "What is MCP?",
            "findings": "",
            "review": "",
            "retry_count": 0,
            "feedback": "",
            "final_report": "",
        })

    assert mock_research.await_count == 1
    assert mock_review.await_count == 1
    assert mock_writer.await_count == 1
    assert result["final_report"] == "# Final Report"


@pytest.mark.asyncio
async def test_workflow_retries_and_stops_after_two_retries():
    with (
        patch(
            "src.agents.workflow.research",
            new_callable=AsyncMock,
            return_value="Updated research findings",
        ) as mock_research,
        patch(
            "src.agents.workflow.review_research",
            new_callable=AsyncMock,
            return_value=(
                "ASSESSMENT: Incomplete\n"
                "MISSING INFORMATION: Explain the missing details\n"
                "RECOMMENDATION: NEEDS_MORE_RESEARCH"
            ),
        ) as mock_review,
        patch(
            "src.agents.workflow.write_report",
            new_callable=AsyncMock,
            return_value="# Final Report",
        ) as mock_writer,
    ):
        workflow = build_workflow()

        result = await workflow.ainvoke({
            "question": "What is MCP?",
            "findings": "",
            "review": "",
            "retry_count": 0,
            "feedback": "",
            "final_report": "",
        })

    assert mock_research.await_count == 3
    assert mock_review.await_count == 3
    assert mock_writer.await_count == 1
    assert result["retry_count"] == 2
    assert result["final_report"] == "# Final Report"
    assert "Explain the missing details" in mock_research.await_args_list[1].args[0]
