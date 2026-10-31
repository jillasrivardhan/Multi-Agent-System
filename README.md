# ResearchMind — Multi-Stage AI Research Assistant

ResearchMind is a Streamlit-based AI research application that turns a topic into a structured research report. It combines web search, webpage extraction, LLM-based analysis, report generation, and review in a staged workflow.

## Overview

Instead of relying on a single prompt to produce a report, ResearchMind separates the work into stages:

1. **Search** — creates a focused search query and retrieves web results through Tavily.
2. **Read** — extracts content from selected webpages and analyzes the material relevant to the topic.
3. **Write** — converts the research findings into a readable report.
4. **Critique** — reviews the generated report and provides a final quality check.

The Streamlit interface presents the research workflow and its outputs.

## Key Features

- Topic-driven research workflow.
- Web search using the Tavily API.
- Webpage content extraction using `requests` and `BeautifulSoup`.
- Separate LLM chains for search-query generation, research analysis, report writing, and review.
- Streamlit interface for running the pipeline and viewing stage outputs.
- Environment-variable configuration for API credentials.
- Modular code structure separating the UI, agents/chains, and tools.

## Workflow

```text
User enters a research topic
            |
            v
     Search-query chain
            |
            v
      Tavily web search
            |
            v
     Select relevant URLs
            |
            v
  Scrape pages with requests
       and BeautifulSoup
            |
            v
      Reader / analysis chain
            |
            v
        Writer chain
            |
            v
        Critic chain
            |
            v
      Final research output
```

## Tech Stack

| Component | Technology |
|---|---|
| User interface | Streamlit |
| LLM orchestration | LangChain |
| LLM provider | Groq or Google Gemini, depending on configuration |
| Web search | Tavily |
| Webpage extraction | Requests, BeautifulSoup |
| Configuration | python-dotenv |

> The selected model and provider depend on the values configured in your environment and the model initialization in `Agents/agents.py`.

## Project Structure

```text
ResearchMind/
│
├── Agents/
│   └── agents.py          # LLM setup and prompt chains
│
├── Tools/
│   └── tools.py           # Tavily search and webpage scraping tools
│
├── app.py                 # Streamlit user interface and pipeline execution
├── .env                   # API keys (do not commit)
├── .gitignore
└── requirements.txt
```

Your local project may contain additional files. Update this structure to match the repository before publishing.

## Setup and Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd ResearchMind
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -3.11 -m venv project
.\project\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv project
source project/bin/activate
```

### 3. Install dependencies

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

Install the core packages if they are not already listed:

```bash
pip install streamlit langchain langchain-core langchain-groq langchain-google-genai tavily-python requests beautifulsoup4 python-dotenv
```

### 4. Configure environment variables

Create a `.env` file in the project root.

For a Groq configuration:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_supported_groq_model
TAVILY_API_KEY=your_tavily_api_key
```

For a Gemini configuration:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Use the provider and variable names expected by your current `Agents/agents.py`. Do not put real API keys in source code or commit your `.env` file.

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will print a local URL in the terminal. Open that URL in your browser.

## Configuration Notes

- Choose a model that is currently available to your account and check its rate limits.
- Keep scraped webpage content bounded. Sending several full webpages to every chain can cause token-limit errors.
- Limit the number of search results and scraped URLs to what the task needs.
- Set output-token limits appropriate to each stage.
- Handle failed or inaccessible webpages gracefully.
- API quotas and pricing depend on the provider, model, account tier, and current provider policies.

## Security

- Store API keys in `.env`.
- Add `.env` and virtual-environment folders to `.gitignore`.
- Never publish API keys, access tokens, or private configuration.
- Treat webpage text as untrusted input. Web content can contain prompt-injection instructions; do not let scraped content override the system's intended instructions.
- Consider a dedicated prompt-injection detection layer, such as Prompt Guard, as an additional security measure. It is not a replacement for the main language model.

Suggested `.gitignore`:

```gitignore
.env
.venv/
venv/
project/
__pycache__/
*.pyc
.streamlit/secrets.toml
```

## Current Scope and Limitations

- Search quality depends on Tavily results and the search query generated by the model.
- Scraping depends on website accessibility, page structure, and anti-bot restrictions.
- The quality and factual reliability of the report depend on the sources retrieved and the model's analysis.
- The application should retain source URLs alongside extracted content so readers can verify claims.
- Provider rate limits can interrupt a run. Reducing input size, limiting scraped pages, and using a model with suitable quotas can help.

## Future Improvements

- Add source citations directly to report claims.
- Add configurable search-result and scraping limits in the UI.
- Add token and execution-time monitoring for each stage.
- Add retry logic and provider fallback when a model request fails.
- Add prompt-injection checks for retrieved webpages.
- Add export options such as Markdown and PDF.
- Add an evaluation step to assess source relevance and report quality.

## Contributing

Contributions, suggestions, and improvements are welcome. Open an issue to discuss a proposed change or submit a pull request.

## Disclaimer

ResearchMind is an AI-assisted research tool. Always verify important claims against the original sources. Generated content may contain omissions or inaccuracies.
