from langchain.tools import tool
from pydantic import BaseModel, Field
from tavily import TavilyClient
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import os

load_dotenv()

# Tavily client
api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError("TAVILY_API_KEY is missing from .env")

tavily = TavilyClient(api_key=api_key)


# Search tool input schema
class WebSearchInput(BaseModel):
    query: str = Field(
        description="A single complete web search query."
    )


# Scraper tool input schema
class ScrapeURLInput(BaseModel):
    url: str = Field(
        description="A complete HTTP or HTTPS webpage URL."
    )


@tool(args_schema=WebSearchInput)
def web_search(query: str) -> str:
    """
    Search the web using Tavily.
    Returns titles, URLs and relevant snippets.
    """

    try:
        results = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )

        output = []

        for item in results.get("results", []):

            output.append(
                f"Title: {item.get('title', 'N/A')}\n"
                f"URL: {item.get('url', 'N/A')}\n"
                f"Content: {item.get('content', '')[:600]}\n"
            )

        if not output:
            return "No search results found."

        return "\n--------------------\n".join(output)

    except Exception as e:
        return f"Search error: {str(e)}"


@tool(args_schema=ScrapeURLInput)
def scrape_url(url: str) -> str:
    """
    Scrape a webpage and return clean text content.
    """

    try:
        if not url.startswith(("http://", "https://")):
            return "Invalid URL provided."

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary HTML elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside"
        ]):
            tag.decompose()

        content = soup.get_text(
            separator=" ",
            strip=True
        )

        return content[:6000]

    except requests.exceptions.RequestException as e:
        return f"Scraping error: {str(e)}"

    except Exception as e:
        return f"Unexpected scraping error: {str(e)}"