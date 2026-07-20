from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Absolute path to rag/chroma_db
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "chroma_db"

pdfs = [
    "data/business_policies.pdf",
    "data/pricing_rules.pdf",
    "data/service_catalog.pdf",
    "data/surcharge_rules.pdf"
]

docs = []

for pdf in pdfs:
    loader = PyPDFLoader(pdf)
    docs.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(DB_PATH)
)

print(f"Stored {len(chunks)} chunks")
print(f"Database saved at: {DB_PATH}")