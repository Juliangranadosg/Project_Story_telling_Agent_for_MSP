import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "Content Drafts")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "msp-content-agent")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200

DATA_FOLDER = "data"

def check_environment_variables():
    if not OPENAI_API_KEY:
        raise ValueError("Missing OPENAI_API_KEY in .env file")

    if not PINECONE_API_KEY:
        raise ValueError("Missing PINECONE_API_KEY in .env file")

    if not PINECONE_INDEX_NAME:
        raise ValueError("Missing PINECONE_INDEX_NAME in .env file")

    if not TAVILY_API_KEY:
        raise ValueError("Missing TAVILY_API_KEY in .env file")
    
    if not AIRTABLE_API_KEY:
        raise ValueError("Missing AIRTABLE_API_KEY in .env file")

    if not AIRTABLE_BASE_ID:
        raise ValueError("Missing AIRTABLE_BASE_ID in .env file")

    print("Environment variables loaded successfully.")