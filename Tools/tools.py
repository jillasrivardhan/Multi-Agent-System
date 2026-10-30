"""Tools for multi agent systems."""

from tavily import TavilyClient
import os
from rich import print
from bs4 import BeautifulSoup
import requests

def web_search_tool(query: str) -> str:
    """Search the web for a query and return the results."""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query,max_results=5)
    return "\n\n".join(f"Title: {result['title']}\nURL: {result['url']}\n Content: {result['content'][:500]}..." for result in response['results'])



def web_scraper_tool(url: str) -> str:
    """Scrape the content of a web page by using the urlsand return the text."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        for script in soup(["script", "style", "header", "footer", "nav", "aside", "form", "input", "button","div", "span", "img", "svg", "canvas", "video", "audio"]):
            script.decompose() 
        return f"Scraped content from '{url}': {text[:800]}..."  
    except requests.exceptions.RequestException as e:
        return f"Error scraping '{url}': {e}"
