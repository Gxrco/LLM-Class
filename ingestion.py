from dotenv import load_dotenv
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from firecrawl import FirecrawlApp
from langchain.schema import Document

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")


def ingest_with_firecrawl() -> None:
    app = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
    url = "https://minecraft.fandom.com/es/wiki/Minecraft"

    page_content = app.scrape_url(url=url, 
                                        params={"onlyMainContent": True})
    print(page_content)
    doc = Document(page_content=str(page_content), metadata={"source": url})

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    docs = text_splitter.split_documents([doc])

    PineconeVectorStore.from_documents(
        docs, embeddings, index_name=os.environ["INDEX_NAME"]
    )

if __name__ == "__main__":
    ingest_with_firecrawl()

