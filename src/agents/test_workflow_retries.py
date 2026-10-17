
import asyncio
from unittest.mock import AsyncMock, patch

from src.agents.workflow import build_workflow


async def main():
    workflow = build_workflow()

    # Simulate two requests for more research, then acceptance.
    mocked_reviews = [
        "ASSESSMENT: Partially answered.\n"
        "MISSING INFORMATION: First gap.\n"
        "RECOMMENDATION: NEEDS_MORE_RESEARCH",

        "ASSESSMENT: Partially answered.\n"
        "MISSING INFORMATION: Second gap.\n"
        "RECOMMENDATION: NEEDS_MORE_RESEARCH",

        "ASSESSMENT: Answered adequately.\n"
        "MISSING INFORMATION: None identified.\n"
        "RECOMMENDATION: ACCEPT",
    ]

    with patch(
        "src.agents.workflow.review_research",
        new_callable=AsyncMock,
        side_effect=mocked_reviews,
    ) as mock_review:
        with patch(
            "src.agents.workflow.research",
            new_callable=AsyncMock,
            side_effect=[
                "Initial findings",
                "Findings addressing the first gap",
                "Findings addressing the second gap",
            ],
        ) as mock_research:
            result = await workflow.ainvoke({
                "question": "Test question",
                "findings": "",
                "review": "",
                "retry_count": 0,
                "feedback": "",
            })

    print("Research calls:", mock_research.await_count)
    print("Review calls:", mock_review.await_count)
    print("Retry count:", result["retry_count"])
    print("Final review:", result["review"])

    assert mock_research.await_count == 3
    assert mock_review.await_count == 3
    assert result["retry_count"] == 2
    assert "ACCEPT" in result["review"]
    assert "NEEDS_MORE_RESEARCH" not in result["review"]

    print("\nPASS: Two retries occurred, then the workflow accepted.")


if __name__ == "__main__":
    asyncio.run(main())
