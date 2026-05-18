from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from config import PINECONE_API_KEY, PINECONE_INDEX_NAME, EMBEDDING_MODEL


def create_pinecone_index():
    pc = Pinecone(api_key=PINECONE_API_KEY)

    existing_indexes = pc.list_indexes().names()

    if PINECONE_INDEX_NAME not in existing_indexes:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

        print(f"Created Pinecone index: {PINECONE_INDEX_NAME}")

    else:
        print(f"Pinecone index already exists: {PINECONE_INDEX_NAME}")


def get_embeddings():
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL
    )


def create_vectorstore_from_documents(chunks):
    embeddings = get_embeddings()

    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME
    )

    return vectorstore


def connect_to_existing_vectorstore():
    embeddings = get_embeddings()

    vectorstore = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings
    )

    return vectorstore