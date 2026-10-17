
import asyncio
from unittest import result
from dotenv import load_dotenv

from src.agents.workflow import build_workflow


async def main():
    load_dotenv()

    workflow = build_workflow()

    initial_state = {
    "question": "What is the Model Context Protocol?",
    "findings": "",
    "review": "",
    "retry_count": 0,
    "feedback": "",
}

    print("Starting research workflow...\n")

    result = await workflow.ainvoke(initial_state)

    print("Retry count:", result["retry_count"])
    print("Final recommendation:", result["review"].split("RECOMMENDATION:")[-1].strip())

    print("=== RESEARCH FINDINGS ===")
    print(result["findings"])

    print("\n=== REVIEW ===")
    print(result["review"])


if __name__ == "__main__":
    asyncio.run(main())
