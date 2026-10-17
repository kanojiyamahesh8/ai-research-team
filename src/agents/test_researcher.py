
import asyncio

from dotenv import load_dotenv

from src.agents.researcher import research


async def main():
    load_dotenv()

    question = "What is the Model Context Protocol, according to our documents?"

    print("Research question:", question)
    print("\nResearching...\n")

    answer = await research(question)

    print("Researcher's answer:")
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())
