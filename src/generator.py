from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config import CHAT_MODEL
from retriever import retrieve_documents, format_docs, print_retrieved_sources
from internet_research import collect_online_research, format_online_sources


def get_llm():
    llm = ChatOpenAI(
        model=CHAT_MODEL,
        temperature=0.2
    )

    return llm


content_prompt = ChatPromptTemplate.from_template("""
You are an expert content strategist and Mental Space Psychology communication assistant.

Your task:
Create source-based content from the retrieved local source context and supporting online research.

Important source rules:
- The local uploaded documents are the primary trusted source.
- The online sources are supporting sources only.
- Do not invent facts.
- Do not make exaggerated therapeutic claims.
- Do not promise healing, trauma resolution, or guaranteed outcomes.
- Keep the language clear, professional, warm, and understandable for non-experts.
- The content is for human review, not automatic publishing.
- Include source references at the end.
- Keep the simple exercise safe, light, and public-friendly.
- Do not include trauma work, deep therapeutic interventions, or diagnostic claims.

Topic:
{topic}

Local retrieved source context:
{local_context}

Supporting online research:
{online_context}

Create the following output taking into account the relevant format for each platform:

1. Expert Summary
2. Public-Friendly Explanation
3. Instagram Caption
4. LinkedIn Post for professional Linkedin audience
5. 5-Slide Carousel Outline
6. 3 Hook Ideas
7. SEO Keywords
8. Hashtags
9. Gentle CTA
10. Simple Safe Exercise
11. Source References
""")


def ask_msp_agent(topic: str):
    retrieved_docs = retrieve_documents(topic)
    local_context = format_docs(retrieved_docs)

    print_retrieved_sources(retrieved_docs)

    online_sources = collect_online_research(topic, max_results=5)
    online_context = format_online_sources(online_sources)

    print("\nOnline sources collected:")
    for source in online_sources:
        print("-", source["title"])
        print(" ", source["url"])

    llm = get_llm()
    chain = content_prompt | llm

    response = chain.invoke({
        "topic": topic,
        "local_context": local_context,
        "online_context": online_context
    })

    return response.content