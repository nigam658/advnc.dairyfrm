from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np

from app.databases.chromadb import collection

def read_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    all_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text :
            all_text += text

    return all_text

def chunk_text (text: str, chunk_size = 500):

    chunks = []

    for i in range(0, len(text),chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks

def add_pdf_to_db():

    pdf_text = read_pdf("documents/Good-Dairy-husbandry-practices.pdf")

    chunks=chunk_text(pdf_text)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    Embeddings = model.encode(chunks)

    print(type(Embeddings))

    collection.add(
        documents=chunks,
        embeddings=Embeddings.tolist(),
        ids=[str(i) for i in range(len(chunks))]
    )

    return "PDF added to database successfully"









