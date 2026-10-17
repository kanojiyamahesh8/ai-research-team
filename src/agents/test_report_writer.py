
import asyncio

from src.agents.report_writer import write_report


async def main():
    question = "What is the Model Context Protocol (MCP)?"

    findings = """
    MCP is a protocol that allows AI applications to discover
    and invoke tools exposed by external servers through a
    standardized interface.
    """

    review = """
    Assessment: Answered adequately.
    Missing information: None identified.
    Recommendation: ACCEPT
    """

    print("Generating research report...\n")

    report = await write_report(
        question=question,
        findings=findings,
        review=review,
    )

    print("=== FINAL RESEARCH REPORT ===\n")
    print(report)


if __name__ == "__main__":
    asyncio.run(main())
