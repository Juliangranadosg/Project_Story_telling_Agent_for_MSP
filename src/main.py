from config import DATA_FOLDER
from document_loader import load_documents
from chunker import split_documents
from vectorstore import create_pinecone_index, create_vectorstore_from_documents
from topic_manager import get_next_topic
from generator import ask_msp_agent


def build_vector_database():
    print("Loading documents...")
    documents = load_documents(DATA_FOLDER)
    print(f"Loaded {len(documents)} documents.")

    print("Splitting documents into chunks...")
    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    print("Creating Pinecone index...")
    create_pinecone_index()

    print("Uploading chunks to Pinecone...")
    create_vectorstore_from_documents(chunks)

    print("Vector database is ready.")


def run_agent():
    topic = get_next_topic()

    print("Selected topic:")
    print(topic)

    print("\nGenerating content...\n")
    result = ask_msp_agent(topic)

    print(result)


if __name__ == "__main__":
    # Run this only when you want to upload/re-upload documents:
    #build_vector_database()

    # Run the agent:
    run_agent()