from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Absolute path to rag/chroma_db
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory=str(DB_PATH),
    embedding_function=embeddings
)

print("Database Path:", DB_PATH)
print("Documents in DB:", db._collection.count())


def retrieve(query: str):
    docs = db.similarity_search(query, k=2)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    return context