
import asyncio
from dotenv import load_dotenv

from src.agents.reviewer import review_research


async def main():
    load_dotenv()

    question = "What is the Model Context Protocol?"

    findings = """
    Our document says MCP is a protocol that allows AI applications
    to discover and invoke tools exposed by external servers through
    a standardized interface.
    """

    print("Original question:", question)
    print("\nResearch findings:", findings)
    print("\nReviewing...\n")

    review = await review_research(question, findings)

    print("Reviewer's assessment:")
    print(review)


if __name__ == "__main__":
    asyncio.run(main())
