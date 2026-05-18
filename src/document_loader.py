import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def load_documents(folder_path: str):
    documents = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            docs = loader.load()

        elif filename.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
            docs = loader.load()

        else:
            continue

        for doc in docs:
            doc.metadata["source"] = filename

        documents.extend(docs)

    return documents