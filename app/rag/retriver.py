from sentence_transformers import SentenceTransformer

from app.databases.chromadb import collection



model = SentenceTransformer("all-MiniLM-L6-v2")

def retriever_chunks(question):

    Embeddings_question = model.encode(question)

    result = collection.query(
        query_embeddings=[Embeddings_question.tolist()],
        n_results=3
    )
    return result["documents"]


def retrieve_text(question):

    chunks = retriever_chunks(question)
    return "\n".join(chunks[0])

    

