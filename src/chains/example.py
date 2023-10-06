import os
from dotenv import load_dotenv
from langchain import LLMMathChain, OpenAI

load_dotenv()

llm = OpenAI(temperature=0)
chain = LLMMathChain(llm=llm, verbose=True)