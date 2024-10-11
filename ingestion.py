from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from consts import INDEX_NAME
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")


def ingest_docs():
    loader = ReadTheDocsLoader("docs.python.org/3.10")
    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} raw documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)
    print(f"split {len(documents)} documents")

    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("docs.python.org", "https://docs.python.org")
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} to Pinecone")
    PineconeVectorStore.from_documents(
        documents, embeddings, index_name=INDEX_NAME
    )


if __name__ == "__main__":
    ingest_docs()
