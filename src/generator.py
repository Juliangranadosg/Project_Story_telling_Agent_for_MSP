from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config import CHAT_MODEL
from retriever import retrieve_documents, format_docs


def get_llm():
    return ChatOpenAI(
        model=CHAT_MODEL,
        temperature=0.3
    )


content_prompt = ChatPromptTemplate.from_template("""
You are an expert content strategist and Mental Space Psychology communication assistant.

Your task:
Create source-based content from the retrieved context.

Important rules:
- Use ONLY the provided source context.
- Do not invent facts.
- Do not make exaggerated therapeutic claims.
- Do not promise healing, trauma resolution, or guaranteed outcomes.
- Keep the language clear, professional, warm, and understandable for non-experts.
- The content is for human review, not automatic publishing.
- Include source references at the end.

Topic:
{topic}

Retrieved source context:
{context}

Create the following output:

1. Expert Summary
2. Public-Friendly Explanation
3. Instagram Caption
4. LinkedIn Post
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
    context = format_docs(retrieved_docs)

    llm = get_llm()
    chain = content_prompt | llm

    response = chain.invoke({
        "topic": topic,
        "context": context
    })

    return response.content