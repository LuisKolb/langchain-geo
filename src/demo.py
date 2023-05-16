from langchain.document_loaders import PlaywrightURLLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

urls = [
    "https://thesaurus.geolba.ac.at/?uri=http://resource.geolba.ac.at/minres/28&lang=de",
    "https://thesaurus.geolba.ac.at/?uri=http://resource.geolba.ac.at/minres/83&lang=de",
    "https://thesaurus.geolba.ac.at/?uri=http://resource.geolba.ac.at/minres/78&lang=de"
]

loader = PlaywrightURLLoader(urls=urls, remove_selectors=["header", "footer", "#navBar", "#pageFooter", "#appsCard", "#search_widget"], headless=True)

data = loader.load()

print(data)

from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(data)

from langchain.embeddings import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

from langchain.vectorstores import Chroma
db = Chroma.from_documents(texts, embeddings)

retriever = db.as_retriever()

qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)

query = "what are some rocks you know?"
print(qa.run(query))

