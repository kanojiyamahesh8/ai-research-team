
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from src.agents.researcher import research
from src.agents.reviewer import review_research


class ResearchState(TypedDict):
    question: str
    findings: str
    review: str
    retry_count: int


async def researcher_node(state: ResearchState) -> dict:
    """Research the question and store the findings."""

    findings = await research(state["question"])

    return {"findings": findings}


async def reviewer_node(state: ResearchState) -> dict:
    """Review the findings and store the review."""

    review = await review_research(
        state["question"],
        state["findings"],
    )

    return {"review": review}


def build_workflow():
    """Build the initial Researcher → Reviewer workflow."""

    graph = StateGraph(ResearchState)

    graph.add_node("researcher", researcher_node)
    graph.add_node("reviewer", reviewer_node)

    graph.add_edge(START, "researcher")
    graph.add_edge("researcher", "reviewer")
    graph.add_edge("reviewer", END)

    return graph.compile()
