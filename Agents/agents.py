

from click import prompt
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool
from Tools.tools import web_search_tool, web_scraper_tool
from Prompts.prompts import prompt


llm = ChatGroq(
    model="gpt-4o",
    temperature=0.7,
    )

agent = create_agent(
    model=llm,
    tools = [web_search_tool, web_scraper_tool],
    system_prompt=prompt,
)
