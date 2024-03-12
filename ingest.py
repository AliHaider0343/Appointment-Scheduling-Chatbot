from langchain.embeddings import OpenAIEmbeddings,HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import JSONLoader,TextLoader,CSVLoader
import openai
load_dotenv()
import os 
openai.api_key = os.getenv('OPENAI_API_KEY')
def api_key():
    return os.getenv("OPENAI_API_KEY")



def refresh_db(doc_dir="E:\COURSES\MACHINE_LEARNING\MAKTEK.IO\Appointment_booking_module\Appointment_data.csv",persist_dir="./appointment_vec_db",embedding_function=OpenAIEmbeddings(chunk_size=2)):
    #loader=JSONLoader(doc_dir,jq_schema=".customers[].content'")
    loader=CSVLoader(doc_dir)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    docs = text_splitter.split_documents(documents)


    #to store embeddings in vectordatabase 
    chroma_db = Chroma.from_documents(
    documents = docs,
    embedding = embedding_function,
    persist_directory=persist_dir
    )

#######################################################################

def load_vec_db(persit_dir="./appointment_vec_db",embedding_function=OpenAIEmbeddings()):
    vector_store = Chroma(persist_directory=persit_dir, embedding_function=embedding_function)
    return vector_store.as_retriever()







