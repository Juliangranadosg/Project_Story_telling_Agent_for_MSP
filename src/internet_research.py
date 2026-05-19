from tavily import TavilyClient
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config import TAVILY_API_KEY, CHAT_MODEL


def get_tavily_client():
    return TavilyClient(api_key=TAVILY_API_KEY)


def web_search(topic: str, max_results: int = 5):
    client = get_tavily_client()

    query = f"""
    Mental Space Psychology, Social Panorama, future vision, coaching,
    clarity, identity, relationships, decision-making: {topic}
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_answer=False,
        include_raw_content=False
    )

    results = response.get("results", [])

    sources = []

    for result in results:
        sources.append({
            "title": result.get("title", "No title"),
            "url": result.get("url", ""),
            "content": result.get("content", ""),
            "source_type": "web"
        })

    return sources


def summarize_online_sources(topic: str, sources: list):
    if not sources:
        return []

    llm = ChatOpenAI(
        model=CHAT_MODEL,
        temperature=0.2
    )

    prompt = ChatPromptTemplate.from_template("""
You are an expert research assistant for a Mental Space Psychology content agent.

Your task:
Summarize the online source below for use in human-reviewed content creation.

Rules:
- Do not exaggerate claims.
- Do not make therapeutic promises.
- Focus on information that is relevant to the topic.
- Keep the summary short and clear.
- Mention why this source may be useful.
- If the source is only loosely related, say so.

Topic:
{topic}

Source title:
{title}

Source URL:
{url}

Source content:
{content}

Return:

1. Short Summary
2. Relevant Ideas
3. Usefulness for Content Creation
4. Source URL
""")

    chain = prompt | llm

    summarized_sources = []

    for source in sources:
        response = chain.invoke({
            "topic": topic,
            "title": source["title"],
            "url": source["url"],
            "content": source["content"]
        })

        summarized_sources.append({
            "title": source["title"],
            "url": source["url"],
            "summary": response.content,
            "source_type": source["source_type"]
        })

    return summarized_sources


def format_online_sources(summarized_sources: list):
    if not summarized_sources:
        return "No online sources found."

    formatted = []

    for i, source in enumerate(summarized_sources, start=1):
        formatted.append(
            f"[Online Source {i}]\n"
            f"Title: {source['title']}\n"
            f"URL: {source['url']}\n"
            f"Type: {source['source_type']}\n"
            f"Summary:\n{source['summary']}"
        )

    return "\n\n".join(formatted)


def collect_online_research(topic: str, max_results: int = 5):
    print("\nSearching the internet...")
    raw_sources = web_search(topic, max_results=max_results)

    print(f"Found {len(raw_sources)} online sources.")

    print("\nSummarizing online sources...")
    summarized_sources = summarize_online_sources(topic, raw_sources)

    return summarized_sources


def run_internet_research(topic: str, max_results: int = 5):
    """
    Wrapper function used by generator.py.

    This keeps the existing code structure unchanged,
    but gives generator.py the function name it expects.
    """
    return collect_online_research(topic, max_results=max_results)