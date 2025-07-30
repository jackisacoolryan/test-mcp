from typing import List, Dict, Any, TypedDict
from fastmcp import FastMCP

# Example documents for search and fetch
DOCUMENTS = [
    {
        "id": "1",
        "title": "FastMCP Introduction",
        "text": "This document introduces FastMCP and explains how to build MCP servers.",
        "url": "https://example.com/fastmcp-intro",
    },
    {
        "id": "2",
        "title": "Model Context Protocol",
        "text": "The Model Context Protocol defines a contract for connecting LLMs to external data via search and fetch tools.",
        "url": "https://example.com/mcp-spec",
    },
]

class SearchResult(TypedDict):
    id: str
    title: str
    text: str
    url: str

class FetchResult(TypedDict):
    id: str
    title: str
    text: str
    url: str
    metadata: Dict[str, Any]

# Create MCP server instance
mcp = FastMCP("Test MCP Server")

@mcp.tool
def search(query: str) -> List[SearchResult]:
    """
    Search documents. Return up to 5 results containing the query.
    Each result includes id, title, a relevant text snippet and url.
    """
    results: List[SearchResult] = []
    query_lower = query.lower()
    for doc in DOCUMENTS:
        if query_lower in doc["text"].lower() or query_lower in doc["title"].lower():
            snippet = doc["text"]
            if len(snippet) > 200:
                snippet = snippet[:200] + "..."
            results.append({
                "id": doc["id"],
                "title": doc["title"],
                "text": snippet,
                "url": doc["url"],
            })
            if len(results) >= 5:
                break
    return results

@mcp.tool
def fetch(doc_id: str) -> FetchResult:
    """
    Fetch full document contents by id. Returns an object with id, title, text, url and optional metadata.
    """
    for doc in DOCUMENTS:
        if doc["id"] == doc_id:
            return {
                "id": doc["id"],
                "title": doc["title"],
                "text": doc["text"],
                "url": doc["url"],
                "metadata": {},
            }
    # Not found: return empty fields
    return {
        "id": "",
        "title": "",
        "text": "",
        "url": "",
        "metadata": {},
    }

if __name__ == "__main__":
    import os
    # Use port from environment variable PORT or default to 8000
    port = int(os.environ.get("PORT", "8000"))
    # Host 0.0.0.0 to accept external connections
    mcp.run(transport="http", host="0.0.0.0", port=port)
