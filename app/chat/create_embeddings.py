from langchain.document_loaders import PyPDFLoader # allows to load the PDF File and Extract the text from it
from langchain.text_splitter import RecursiveCharacterTextSplitter # allow us to specify the chunks of text that we want to extract from a larger body of text
from app.chat.vector_stores.pinecone import vector_store

# Error Handling
import io
import sys 
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def create_embeddings_for_pdf(pdf_id: str, pdf_path: str):
    """
    Generate and store embeddings for the given pdf

    1. Extract text from the specified PDF.
    2. Divide the extracted text into manageable chunks.
    3. Generate an embedding for each chunk.
    4. Persist the generated embeddings.

    :param pdf_id: The unique identifier for the PDF.
    :param pdf_path: The file path to the PDF.

    Example Usage:

    create_embeddings_for_pdf('123456', '/path/to/pdf')
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    loader = PyPDFLoader(pdf_path)

    # extract all the text and break up into chunks
    docs = loader.load_and_split(text_splitter)

    for doc in docs:
        doc.metadata = {
            "page": doc.metadata["page"],
            "text": doc.page_content,
            "pdf_id": pdf_id,
        }

    vector_store.add_documents(docs)

    print(docs)
