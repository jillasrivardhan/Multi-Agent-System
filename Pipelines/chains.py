


from Agents.agents import web_search, web_scraper 

def run_web_search_and_scraper_agent(query: str, url: str) -> str:
    """
    Run a web search using the web_search function from Agents.agents and also scrape a website using the web_scraper function from Agents.agents.

    Args:
        query (str): The search query.
        url (str): The URL of the website to scrape.

    Returns:
       str: The search results.
      """
    return [web_search(query), web_scraper(url)]


