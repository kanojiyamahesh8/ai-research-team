
import asyncio
from unittest.mock import AsyncMock, patch

from src.agents.workflow import build_workflow


async def main():
    with (
        patch(
            "src.agents.workflow.research",
            new_callable=AsyncMock,
            return_value="Research findings from the local documents.",
        ) as mock_research,
        patch(
            "src.agents.workflow.review_research",
            new_callable=AsyncMock,
            return_value=(
                "ASSESSMENT: The question is answered adequately.\n"
                "MISSING INFORMATION: None identified\n"
                "RECOMMENDATION: ACCEPT"
            ),
        ) as mock_review,
        patch(
            "src.agents.workflow.write_report",
            new_callable=AsyncMock,
            return_value="# Test Research Report\n\nFinal report generated.",
        ) as mock_report,
    ):
        workflow = build_workflow()

        initial_state = {
            "question": "What is MCP?",
            "findings": "",
            "review": "",
            "retry_count": 0,
            "feedback": "",
            "final_report": "",
        }

        result = await workflow.ainvoke(initial_state)

        assert mock_research.await_count == 1
        assert mock_review.await_count == 1
        assert mock_report.await_count == 1
        assert result["retry_count"] == 0
        assert result["final_report"] == (
            "# Test Research Report\n\nFinal report generated."
        )

        print("Research calls:", mock_research.await_count)
        print("Review calls:", mock_review.await_count)
        print("Report writer calls:", mock_report.await_count)
        print("Final report:", result["final_report"])
        print("\nPASS: The complete workflow ran without real API calls.")


if __name__ == "__main__":
    asyncio.run(main())
