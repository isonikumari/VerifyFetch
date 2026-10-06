from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import os
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for evidence about a claim. Returns titles, URLs, and snippets."""
    results = tavily.search(query=query, max_results=5)
    out = []
    for result in results["results"]:
        out.append(
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Snippet: {result['content'][:300]}"
        )
    return "\n_____\n".join(out)