import sys
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel


# Add the src folder to Python's import path
SRC_DIR = Path(__file__).resolve().parent
sys.path.append(str(SRC_DIR))

from main import run_agent


app = FastAPI()


class ContentRequest(BaseModel):
    topic: str


@app.post("/generate-content")
def generate_content(request: ContentRequest):
    run_agent(topic=request.topic)

    return {
        "success": True,
        "message": "Content draft created in Airtable",
        "topic": request.topic,
        "status": "Needs Review",
    }