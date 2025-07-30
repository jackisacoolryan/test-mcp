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

# Create MCP server instance
mcp = FastMCP("Test MCP Server")

@mcp.tool
def search(query: str):
    """
    Search documents. Return up to 5 results containing the query.
    Each result includes id, title, a relevant text snippet and url.
    """
    results = []
    query_lower = query.lower()
    for doc in DOCUMENTS:
        if query_lower in doc["text"].lower() or query_lower in doc["title"].lower():
            results.append({
                "id": doc["id"],
                "title": doc["title"],
                "text": doc["text"][:200],
                "url": doc["url"]
            })
        if len(results) >= 5:
            break
    return results

@mcp.tool
def fetch(doc_id: str):
    """
    Fetch full document contents by id.
    Returns an object with id, title, text, url, and optional metadata.
    """
    for doc in DOCUMENTS:
        if doc["id"] == doc_id:
            return {
                "id": doc["id"],
                "title": doc["title"],
                "text": doc["text"],
                "url": doc["url"],
                "metadata": {}
            }
    # Not found: return object with empty fields
    return {
        "id": doc_id,
        "title": "",
        "text": "",
        "url": "",
        "metadata": {}
    }

if __name__ == "__main__":
    # Use port from environment variable PORT or default to 8000
    port = int(os.environ.get("PORT", 8000))
    # Host 0.0.0.0 to accept external connections
    mcp.run(transport="http", host="0.0.0.0", port=port)
