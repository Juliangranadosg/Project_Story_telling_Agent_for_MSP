import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from retriever import retrieve_documents, format_docs
from internet_research import run_internet_research, format_online_sources
from config import CHAT_MODEL


def ask_msp_agent(topic: str) -> dict:
    """
    Generates a structured Mental Space Psychology content package.

    Steps:
    1. Retrieve local source documents from Pinecone
    2. Format retrieved documents into text context
    3. Run internet research
    4. Format online sources into text context
    5. Generate structured JSON
    6. Return the JSON as a Python dictionary
    """

    print("Retrieving local MSP sources...")
    local_docs = retrieve_documents(topic)
    local_context = format_docs(local_docs)

    print("Running internet research...")
    online_sources = run_internet_research(topic)
    online_context = format_online_sources(online_sources)

    source_references = online_context

    llm = ChatOpenAI(
        model=CHAT_MODEL,
        temperature=0.2
    )

    prompt = ChatPromptTemplate.from_template("""
You are an expert content strategist and storytelling agent for Mental Space Psychology.

Your task is to create a structured content package based on the topic and the provided sources.

Topic:
{topic}

Local trusted source context:
{local_context}

Online supporting source context:
{online_context}

Source references:
{source_references}

Important rules:
- Use the trusted local sources as the main foundation.
- Use online sources only as supporting information.
- Do not make exaggerated healing claims.
- Do not promise psychological or therapeutic results.
- Keep the language clear, professional, warm, and public-friendly.
- The content should be useful for Instagram, LinkedIn, and human review.
- The simple exercise must be light, safe, and educational.
- Avoid trauma work or deep therapeutic interventions.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations before or after the JSON.

Use exactly this JSON structure:

{{
  "topic": "{topic}",
  "content_angle": "",
  "target_audience": "",
  "source_references": "",
  "expert_summary": "",
  "public_explanation": "",
  "instagram_caption": "",
  "linkedin_post": "",
  "carousel_slides": "",
  "reel_idea": "",
  "hooks": "",
  "seo_keywords": "",
  "hashtags": "",
  "cta": "",
  "simple_exercise": ""
}}
""")

    chain = prompt | llm

    response = chain.invoke({
        "topic": topic,
        "local_context": local_context,
        "online_context": online_context,
        "source_references": source_references
    })

    try:
        content_package = json.loads(response.content)
    except json.JSONDecodeError as error:
        print("\nThe model returned this instead of valid JSON:\n")
        print(response.content)
        raise ValueError(
            "The model did not return valid JSON. "
            "Try running the agent again or make the prompt stricter."
        ) from error

    return content_package