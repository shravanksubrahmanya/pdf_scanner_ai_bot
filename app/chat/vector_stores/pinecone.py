import os
import pinecone
from langchain.vectorstores.pinecone import Pinecone
from app.chat.embeddings.openai import embeddings

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV_NAME"),
)

vector_store = Pinecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"),
    embeddings
)

# vector_store.as_retriever()

# retriever function
def build_retriever(chat_args, k):
    search_kwargs = {
        "filter":{"pdf_id":chat_args.pdf_id},
        # "k":1,  by default k is 1, specifying how many documents should be returned from similarity search
        "k":k,
        }
    return vector_store.as_retriever(
        search_kwargs=search_kwargs,
    )