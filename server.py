from fastmcp import FastMCP
import os

# Example documents for search and fetch
DOCUMENTS = [
    {
        "id": "1",
        "title": "FastMCP Introduction",
        "text": "This document introduces FastMCP and explains how to build MCP servers.",
        "url": "https://example.com/fastmcp-intro"
    },
    {
        "id": "2",
        "title": "Model Context Protocol",
        "text": "The Model Context Protocol defines a contract for connecting LLMs to external data via search and fetch.",
        "url": "https://example.com/mcp-spec"
    },
]

mcp = FastMCP("Test MCP Server")

@mcp.tool
def search(query: str):
    """Search documents. Return up to 5 results containing the query."""
    results = []
    query_lower = query.lower()
    for doc in DOCUMENTS:
        if query_lower in doc["text"].lower() or query_lower in doc["title"].lower():
            results.append({
                "id": doc["id"],
                "title": doc["title"],
                "text": doc["text"][:200],
                "url": doc["url"],
            })
        if len(results) >= 5:
            break
    return results

@mcp.tool
def fetch(doc_id: str):
    """Fetch full document text by id."""
    for doc in DOCUMENTS:
        if doc["id"] == doc_id:
            return {"text": doc["text"], "url": doc["url"]}
    return {"text": "", "url": ""}

if __name__ == "__main__":
    # Use port from environment variable PORT or default to 8000
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)
