
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from src.agents.researcher import research
from src.agents.reviewer import review_research


class ResearchState(TypedDict):
    question: str
    findings: str
    review: str
    retry_count: int
    feedback: str



async def researcher_node(state: ResearchState) -> dict:
    """Research the question, using reviewer feedback on retries."""

    question = state["question"]
    retry_count = state["retry_count"]

    if state["feedback"]:
        question += (
            "\n\nAdditional research requested by the reviewer:\n"
            + state["feedback"]
        )
        retry_count += 1

    findings = await research(question)

    return {
        "findings": findings,
        "retry_count": retry_count,
    }






async def reviewer_node(state: ResearchState) -> dict:
    """Review findings and capture feedback for another attempt."""

    review = await review_research(
        state["question"],
        state["findings"],
    )

    feedback = ""

    if "NEEDS_MORE_RESEARCH" in review:
        if "MISSING INFORMATION:" in review:
            feedback = review.split(
                "MISSING INFORMATION:", 1
            )[1].split(
                "RECOMMENDATION:", 1
            )[0].strip()

    return {
        "review": review,
        "feedback": feedback,
    }




def route_after_review(state: ResearchState) -> str:
    """Retry when requested, but enforce a maximum of two retries."""

    if "NEEDS_MORE_RESEARCH" in state["review"]:
        if state["retry_count"] < 2:
            return "research"

    return "finish"




def build_workflow():
    """Build the Researcher → Reviewer workflow with bounded retries."""

    graph = StateGraph(ResearchState)

    graph.add_node("researcher", researcher_node)
    graph.add_node("reviewer", reviewer_node)

    graph.add_edge(START, "researcher")
    graph.add_edge("researcher", "reviewer")

    graph.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "research": "researcher",
            "finish": END,
        },
    )

    return graph.compile()
