
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AI Research Team")

# Small local dataset for initial testing
DOCUMENTS = {
    "doc1": {
        "title": "Introduction to RAG",
        "content": "Retrieval-Augmented Generation (RAG) combines information retrieval with language generation. It retrieves relevant documents and provides them as context to an LLM."
    },
    "doc2": {
        "title": "Multi-Agent Systems",
        "content": "A multi-agent system uses multiple specialized agents to collaborate on a task. An orchestrator can coordinate their execution and pass information between them."
    },
    "doc3": {
        "title": "Model Context Protocol",
        "content": "MCP is a protocol that allows AI applications to discover and invoke tools exposed by external servers through a standardized interface."
    },
}


@mcp.tool()
def search_documents(query: str) -> list[dict[str, str]]:
    """Search local research documents by matching words in their title or content."""
    words = query.lower().split()
    results = []

    for document_id, document in DOCUMENTS.items():
        searchable_text = (
            document["title"] + " " + document["content"]
        ).lower()

        if any(word in searchable_text for word in words):
            results.append({
                "id": document_id,
                "title": document["title"],
                "content": document["content"],
            })

    return results


@mcp.tool()
def get_document(document_id: str) -> dict[str, str]:
    """Retrieve a research document by its ID, such as doc1."""
    document = DOCUMENTS.get(document_id)

    if document is None:
        return {"error": f"Document '{document_id}' was not found."}

    return {
        "id": document_id,
        "title": document["title"],
        "content": document["content"],
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
