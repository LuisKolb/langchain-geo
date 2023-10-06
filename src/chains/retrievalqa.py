from dotenv import load_dotenv
import chromadb
from langchain import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

#
# CONFIG
#

collection_name = "geo_test"

#
# SETUP
#

load_dotenv()

embedding = OpenAIEmbeddings()

chroma_client = chromadb.HttpClient(host="localhost", port="8000")

lc_client = Chroma(client=chroma_client,
                   collection_name=collection_name,
                   embedding_function=embedding)

retriever = lc_client.as_retriever(search_kwargs={"k": 1})

llm = OpenAI(model_name="text-davinci-003", 
             temperature=0.9, 
             max_tokens=1000)


chain = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type="stuff", 
                                    retriever=retriever,
                                    verbose=True)
