from crewai import LLM
from crewai.tools import tool
from services.web_searcher import WebSearcher
import os

searcher = WebSearcher()
llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)

@tool
def web_search(query: str, num_results: int = 5) -> str:
    """
    Searches the web for a given query using serper.dev and summarizes the findings.

    Args:
        query (str): Search term
        num_results (int): Number of results to fetch

    Returns:
        str: A summary of the findings
    """
    results = searcher.search(query, num_results)

    if not results:
        return "No results found."

    formatted_results = "\n\n".join([
        f"Title: {item['title']}\nSnippet: {item['snippet']}\nLink: {item['link']}"
        for item in results
    ])

    prompt = (
        "Based on the following search results, write a concise summary of the topic:\n\n"
        f"{formatted_results}\n\nSummary:"
    )

    return llm.call(prompt)
