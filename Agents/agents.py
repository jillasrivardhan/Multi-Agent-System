

from click import prompt
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool
from Tools.tools import web_search_tool, web_scraper_tool
from Prompts.prompts import prompt


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7,
    )

web_search_agent = create_agent(
    model=llm,
    tools = [web_search_tool],
    system_prompt=prompt,
)

web_scraper_agent = create_agent(
    model=llm,
    tools = [web_scraper_tool],
    system_prompt=prompt,
)

def web_search(query: str) -> str:
    """
    Perform a web search using the web_search_agent.

    Args:
        query (str): The search query.

    Returns:
        str: The search results.
    """
    return web_search_agent.invoke({"messages": [{"role": "user", "content": query}]}).content

def web_scraper(url: str) -> str:
    """
    Scrape a website using the web_scraper_agent.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        str: The scraped content.
    """
    return web_scraper_agent.invoke({"messages": [{"role": "user", "content": url}]}).content
