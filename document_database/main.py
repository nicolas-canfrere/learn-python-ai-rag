import os
import chromadb
from chromadb import Settings
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

import nltk
nltk.download('punkt_tab', download_dir="./../.venv/nltk_data")
nltk.download('averaged_perceptron_tagger_eng', download_dir="./../.venv/nltk_data")

load_dotenv()

DATA_PATH=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/oauth_rfc"))

def main():
    documents = load_documents()
    chunks = create_chunks(documents)
    embedd_chunks(chunks)


def load_documents() -> list[Document]:
    print("Loading documents...")
    loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    documents = loader.load()

    return documents

def create_chunks(documents: list[Document]) -> list[Document]:
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    # document = chunks[10]
    # print(document.page_content)
    # print(document.metadata)

    return chunks

def init_chromadb() -> None:
    print('Initializing ChromaDB...')
    admin_client = chromadb.AdminClient(
        settings=Settings(
            chroma_api_impl="chromadb.api.fastapi.FastAPI",
            chroma_server_host=os.getenv("CHROMADB_HOST"),
            chroma_server_http_port=int(os.getenv("CHROMADB_PORT"))
        )
    )
    try:
        admin_client.get_tenant(name=os.getenv("CHROMADB_TENANT"))

    except Exception as e:
        admin_client.create_tenant(name=os.getenv("CHROMADB_TENANT"))
        admin_client.create_database(
            name=os.getenv("CHROMADB_DATABASE"),
            tenant=os.getenv("CHROMADB_TENANT")
        )

def embedd_chunks(chunks: list[Document]) -> None:
    print("Initializing ChromaDB...")
    init_chromadb()
    print("Embedding chunks...")
    embedding = OllamaEmbeddings(
        model=os.getenv("OLLAMA_EMBEDDINGS_MODEL"),
        base_url=os.getenv("OLLAMA_BASE_URL")
    )
    try:
        chroma_http_client = chromadb.HttpClient(
            host=os.getenv("CHROMADB_HOST"),
            port=int(os.getenv("CHROMADB_PORT")),
            tenant=os.getenv("CHROMADB_TENANT"),
            database=os.getenv("CHROMADB_DATABASE")
        )
        Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            collection_name=os.getenv("CHROMADB_COLLECTION"),
            client=chroma_http_client,
        )
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    main()