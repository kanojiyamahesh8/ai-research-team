
from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.agents.workflow import build_workflow

app = FastAPI(
    title="AI Research Team API",
    description="API for the multi-agent research workflow",
    version="1.0.0",
)


class ResearchRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="The research question to investigate",
    )


class ResearchResponse(BaseModel):
    question: str
    final_report: str


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    workflow = build_workflow()

    initial_state = {
        "question": request.question,
        "findings": "",
        "review": "",
        "retry_count": 0,
        "feedback": "",
        "final_report": "",
    }

    result = await workflow.ainvoke(initial_state)

    return ResearchResponse(
        question=request.question,
        final_report=result["final_report"],
    )
