import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pgvector import PGVector
import getpass

load_dotenv()

keys = ["GOOGLE_API_KEY", "PGVECTORSTORE"]

for k in keys:
    if not os.environ.get(k):
        os.environ[k] = getpass.getpass(f"{k} not set, please provide:")


CONNECTION_STRING = "postgresql://postgres.lbwprtgtlvvjizebmwtc:NZ6ASpZMwsT5Cw7j@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
COLLECTION_NAME = "rag_documents"


# Load the document from the URL
loader = PyPDFLoader(file_url)
documents = loader.load()

# Split the document into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(documents)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create a PGVector instance and add the documents
# This will create the necessary tables in your database if they don't exist
db = PGVector.from_documents(
    embedding=embeddings,
    documents=splits,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
)

print(f"Successfully stored {len(splits)} document chunks in the PGVector database.")
