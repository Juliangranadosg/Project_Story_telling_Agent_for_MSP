from vectorstore import connect_to_existing_vectorstore


def get_retriever(k: int = 5):
    vectorstore = connect_to_existing_vectorstore()

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )

    return retriever


def retrieve_documents(topic: str, k: int = 5):
    retriever = get_retriever(k=k)

    docs = retriever.invoke(topic)

    if len(docs) == 0:
        raise ValueError("No relevant documents were retrieved from Pinecone.")

    return docs


def format_docs(docs):
    formatted_chunks = []

    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "Unknown source")
        page = doc.metadata.get("page", "N/A")

        formatted_chunks.append(
            f"[Source {i}] File: {source}, Page: {page}\n{doc.page_content}"
        )

    return "\n\n".join(formatted_chunks)


def print_retrieved_sources(docs):
    print("\nSources retrieved:")

    for i, doc in enumerate(docs, start=1):
        print(f"\nSource {i}")
        print("File:", doc.metadata.get("source", "Unknown source"))
        print("Page:", doc.metadata.get("page", "N/A"))
        print("Preview:", doc.page_content[:300])