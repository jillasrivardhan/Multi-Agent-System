from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


# Model setup
llm = ChatGroq(
    model=os.getenv(
        "GROQ_API_KEY",
        "openai/gpt-oss-120b"
    ),
    temperature=0
)


# --------------------------------------------------
# 1. SEARCH AGENT
# --------------------------------------------------

search_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert web research query planner.

        Your task is to convert the user's research topic
        into one effective web search query.

        Rules:
        1. Return only one search query.
        2. Keep the query as a single plain-text string.
        3. Include relevant dates or context when useful.
        4. Do not return JSON.
        5. Do not add explanations or markdown.
        """
    ),
    (
        "human",
        "Create a search query for this topic: {topic}"
    )
])

build_search_agent = lambda: (
    search_prompt | llm | StrOutputParser()
)


# --------------------------------------------------
# 2. READER AGENT
# --------------------------------------------------

reader_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert research analyst.

        Your task is to analyze information extracted
        from webpages.

        Rules:
        1. Identify the most important facts.
        2. Focus on information relevant to the topic.
        3. Remove irrelevant content.
        4. Preserve important dates, names and statistics.
        5. Never invent information.
        6. Mention when information is insufficient.
        """
    ),
    (
        "human",
        """
        Research Topic:
        {topic}

        Search Results:
        {search_results}

        Scraped Webpage Content:
        {scraped_content}

        Analyze the information and provide detailed
        research notes.
        """
    )
])

build_reader_agent = lambda: (
    reader_prompt | llm | StrOutputParser()
)


# --------------------------------------------------
# 3. WRITER CHAIN
# --------------------------------------------------

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert professional research writer.

        Write detailed, factual, structured and insightful
        research reports based on the supplied information.
        """
    ),
    (
        "human",
        """
        Write a detailed research report.

        Topic: {topic}

        Research Gathered:
        {research}

        Follow this structure:

        1. Introduction
        2. Key Findings
           - Minimum 3 well-explained findings
        3. Conclusion
        4. Sources
           - Include all available source URLs.

        Important:
        - Use only the supplied research.
        - Do not invent facts or statistics.
        - Clearly identify missing information.
        - Maintain a professional writing style.
        """
    )
])

writer_chain = (
    writer_prompt
    | llm
    | StrOutputParser()
)


# --------------------------------------------------
# 4. CRITIC CHAIN
# --------------------------------------------------

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a strict and constructive research critic.

        Evaluate research reports based on:
        - Accuracy
        - Relevance
        - Completeness
        - Structure
        - Source quality
        """
    ),
    (
        "human",
        """
        Review the following research report:

        {report}

        Respond in this exact format:

        Score: X/10

        Strengths:
        - ...
        - ...

        Areas to Improve:
        - ...
        - ...

        One line verdict:
        ...
        """
    )
])

critic_chain = (
    critic_prompt
    | llm
    | StrOutputParser()
)