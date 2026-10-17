
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


load_dotenv()


def create_report_writer():
    """Create the agent responsible for writing the final research report."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from the .env file.")

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.2,
        api_key=api_key,
    )

    return llm


async def write_report(question: str, findings: str, review: str) -> str:
    """Write a structured report from the accepted research findings."""

    llm = create_report_writer()

    prompt = f"""
You are the Report Writer in an AI research team.

Write a clear, well-structured research report using the information provided.

Original research question:
{question}

Research findings:
{findings}

Reviewer assessment:
{review}

Instructions:
1. Answer the original question directly.
2. Organize the report with a title, introduction, key findings, and conclusion.
3. Use only claims supported by the research findings.
4. Do not invent facts or sources.
5. If the findings are incomplete, clearly state the limitations.
6. Write in professional, easy-to-understand language.

Final research report:
"""

    response = await llm.ainvoke(prompt)
    return response.content
