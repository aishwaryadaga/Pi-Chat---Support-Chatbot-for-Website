# run only 1st time to store everything in the database

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import pinecone
import asyncio
from langchain.document_loaders.sitemap import SitemapLoader
import constants
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()


def remove_nav_and_header_elements(content: BeautifulSoup) -> str:
    # Find all 'nav' and 'header' elements in the BeautifulSoup object
    nav_elements = content.find_all("nav")
    header_elements = content.find_all("header")

    # Remove each 'nav' and 'header' element from the BeautifulSoup object
    for element in nav_elements + header_elements:
        element.decompose()

    return str(content.get_text())

#Function to fetch data from website
#https://python.langchain.com/docs/modules/data_connection/document_loaders/integrations/sitemap
def get_website_data(sitemap_url):

    loop = asyncio.new_event_loop()
    loader = SitemapLoader(web_path=sitemap_url, continue_on_failure=True)

    docs = loader.load()

    return docs

#Function to split data into smaller chunks
def split_data(docs):

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
    )

    docs_chunks = text_splitter.split_documents(docs)
    return docs_chunks

#Function to create embeddings instance
def create_embeddings():
    # embeddings = SentenceTransformerEmbeddings('all-MiniLM-L6-v2')
    embeddings = OpenAIEmbeddings()
    return embeddings

def push_to_pinecone(pinecone_environment,pinecone_index_name,embeddings,docs):

    pinecone.init(
    environment=pinecone_environment
    )
    # in init function, api key is reqd but we've loaded it from the .env file

    index_name = pinecone_index_name
    index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    return index


url = constants.WEBSITE_URL
docs = get_website_data(url)
print("data retrieved")
docs_chunks = split_data(docs)
print("data split")
embeddings = create_embeddings()
print("embeddings created")
index = push_to_pinecone(constants.PINECONE_ENVIRONMENT,constants.PINECONE_INDEX,embeddings,docs_chunks)
print("pushed to pinecone")