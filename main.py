from Agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain
)

from Tools.tools import web_search, scrape_url

import re


def extract_urls(search_results: str) -> list:

    """Extract URLs from Tavily search results."""

    urls = re.findall(
        r"URL:\s*(https?://[^\s]+)",
        search_results
    )

    # Remove duplicate URLs while preserving order
    return list(dict.fromkeys(urls))


def run_research_pipeline(topic: str) -> dict:

    state = {}

    # ==========================================
    # STEP 1: SEARCH AGENT
    # ==========================================

    print("\n" + "=" * 50)
    print("STEP 1 - SEARCH AGENT")
    print("=" * 50)

    search_agent = build_search_agent()

    print("\nGenerating search query...")

    search_query = search_agent.invoke({
        "topic": topic
    }).strip().strip('"')

    print("\nSearch Query:", search_query)

    print("\nSearching the web using Tavily...")

    search_result = web_search.invoke({
        "query": search_query
    })

    state["search_results"] = search_result

    print("\nSearch Results:\n")
    print(state["search_results"])


    # ==========================================
    # STEP 2: READER AGENT
    # ==========================================

    print("\n" + "=" * 50)
    print("STEP 2 - READER AGENT")
    print("=" * 50)

    urls = extract_urls(state["search_results"])

    # Select top 3 URLs
    selected_urls = urls[:3]

    print("\nSelected URLs:", selected_urls)

    scraped_contents = []

    for index, url in enumerate(selected_urls, start=1):

        print(f"\nScraping resource {index}...")
        print("URL:", url)

        content = scrape_url.invoke({
            "url": url
        })

        scraped_contents.append(
            f"""
            SOURCE {index}
            URL: {url}

            CONTENT:
            {content}
            """
        )

    state["scraped_content"] = "\n\n".join(
        scraped_contents
    )

    if not state["scraped_content"]:
        state["scraped_content"] = (
            "No webpages could be scraped."
        )

    print("\nScraping completed.")

    # Reader agent analyzes extracted content
    reader_agent = build_reader_agent()

    print("\nAnalyzing scraped content...")

    reader_result = reader_agent.invoke({
        "topic": topic,
        "search_results": state["search_results"],
        "scraped_content": state["scraped_content"]
    })

    state["reader_analysis"] = reader_result

    print("\nReader Analysis:\n")
    print(state["reader_analysis"])


    # ==========================================
    # STEP 3: WRITER CHAIN
    # ==========================================

    print("\n" + "=" * 50)
    print("STEP 3 - WRITER")
    print("=" * 50)

    research_combined = f"""
    SEARCH RESULTS:

    {state["search_results"]}

    DETAILED READER ANALYSIS:

    {state["reader_analysis"]}

    SCRAPED CONTENT:

    {state["scraped_content"]}
    """

    print("\nGenerating research report...")

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nFINAL RESEARCH REPORT\n")
    print(state["report"])


    # ==========================================
    # STEP 4: CRITIC CHAIN
    # ==========================================

    print("\n" + "=" * 50)
    print("STEP 4 - CRITIC")
    print("=" * 50)

    print("\nReviewing research report...")

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCRITIC FEEDBACK:\n")
    print(state["feedback"])

    return state


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":

    topic = input(
        "\nEnter a research topic: "
    ).strip()

    if not topic:
        print("Please enter a valid research topic.")

    else:
        try:
            result = run_research_pipeline(topic)

            print("\n" + "=" * 50)
            print("RESEARCH PIPELINE COMPLETED")
            print("=" * 50)

        except Exception as e:
            print("\nResearch pipeline failed!")
            print("Error:", str(e))