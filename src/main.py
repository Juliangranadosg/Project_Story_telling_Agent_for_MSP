import argparse

from config import DATA_FOLDER, check_environment_variables
from document_loader import load_documents
from chunker import split_documents
from vectorstore import create_pinecone_index, create_vectorstore_from_documents
from topic_manager import get_next_topic
from generator import ask_msp_agent
from airtable_writer import create_airtable_record


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


def run_agent(topic=None):
    print("Checking environment variables...")
    check_environment_variables()

    if topic is None:
        topic = get_next_topic()

    print("\nSelected topic:")
    print(topic)

    print("\nGenerating source-based content with local RAG + internet research...\n")
    content_package = ask_msp_agent(topic)

    print("\nGenerated content package:\n")
    print(content_package)

    print("\nSaving content package to Airtable...")
    create_airtable_record(content_package)

    print("\nDone. Draft saved in Airtable with status: Needs Review")

    return content_package


if __name__ == "__main__":

    # ---------------------------------------------------
    # Run this ONLY when you want to upload/re-upload
    # documents and rebuild the Pinecone vector database.
    # Remove the "#" in the next line when needed.
    # ---------------------------------------------------

    # build_vector_database()

    parser = argparse.ArgumentParser(
        description="Run the MSP AI Content Agent."
    )

    parser.add_argument(
        "--topic",
        type=str,
        required=False,
        help="Optional content topic. If not provided, a random topic is selected."
    )

    args = parser.parse_args()

    # Run the content generation agent
    run_agent(topic=args.topic)