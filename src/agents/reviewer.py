
from langchain_groq import ChatGroq


async def review_research(question: str, research_findings: str) -> str:
    """Review research findings and identify missing information."""

    llm = ChatGroq(model="openai/gpt-oss-120b")

    prompt = f"""
You are a careful research reviewer.

Original research question:
{question}

Research findings:
{research_findings}

Evaluate whether the findings adequately answer the original question.

Return your review using these three sections:

ASSESSMENT:
State whether the question is answered adequately or partially.

MISSING INFORMATION:
List important gaps, or write "None identified" if there are no significant gaps.

RECOMMENDATION:
Write either ACCEPT or NEEDS_MORE_RESEARCH, followed by a brief reason.

Base your review only on the supplied research findings.
Do not invent facts or assume that missing information is present.
"""

    response = await llm.ainvoke(prompt)

    return response.content
