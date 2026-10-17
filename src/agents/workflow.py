
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
    """Research the question using reviewer feedback when available."""

    question = state["question"]

    if state["feedback"]:
        question += (
            "\n\nAdditional research requested by the reviewer:\n"
            + state["feedback"]
        )

    findings = await research(question)

    return {"findings": findings}




async def reviewer_node(state: ResearchState) -> dict:
    """Review findings and update feedback and retry count."""

    review = await review_research(
        state["question"],
        state["findings"],
    )

    retry_count = state["retry_count"]
    feedback = ""

    if "NEEDS_MORE_RESEARCH" in review and retry_count < 2:
        retry_count += 1

        if "MISSING INFORMATION:" in review:
            feedback = review.split(
                "MISSING INFORMATION:", 1
            )[1].split(
                "RECOMMENDATION:", 1
            )[0].strip()

    return {
        "review": review,
        "retry_count": retry_count,
        "feedback": feedback,
    }



def route_after_review(state: ResearchState) -> str:
    """Choose the next step based on the review and retry limit."""

    if "ACCEPT" in state["review"] and "NEEDS_MORE_RESEARCH" not in state["review"]:
        return "finish"

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
