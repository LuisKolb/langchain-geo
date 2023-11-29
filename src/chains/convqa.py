from dotenv import load_dotenv
import os
import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from langchain.schema.messages import SystemMessage
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.prompts import MessagesPlaceholder
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents import AgentExecutor
from langchain.chat_models import ChatOpenAI

#
# CONFIG
#

collection_name = "geo_demo"    # collection name in chromaDB
hostname = "chromadb"           # this is the hostname configured in docker-compose.yaml
port = "8000"                   # this is the port configured in docker-compose.yaml
temperature = 0                 # openAI LLM temp
model = 'gpt-3.5-turbo'         # see https://platform.openai.com/docs/models/gpt-3-5 for model selection
verbose_mode = False

#
# SETUP
#

load_dotenv()

def is_docker():
    path = "/proc/self/cgroup"
    return (
        os.path.exists("/.dockerenv")
        or os.path.isfile(path)
        and any("docker" in line for line in open(path))
    )

if not is_docker():
    hostname = "localhost"
    verbose_mode = True 

# client
chroma_client = chromadb.HttpClient(host=hostname, port=port)
lc_client = Chroma(client=chroma_client,
                   collection_name=collection_name,
                   embedding_function=OpenAIEmbeddings())

# LLM
llm = ChatOpenAI(temperature=temperature, model=model, streaming=False)
llm_stream = ChatOpenAI(temperature=temperature, model=model, streaming=True)


# This is needed for both the memory and the prompt
memory_key = "history"
memory = AgentTokenBufferMemory(memory_key=memory_key, llm=llm)
memory_stream = AgentTokenBufferMemory(memory_key=memory_key, llm=llm_stream)

# prompt setup
system_message = SystemMessage(
        content=(
            "Do your best to answer the questions. "
            "You must use the tools available to look up relevant information, if neccessary. "
            "If you use the tools, make sure to always return the URL in addition to the response."
        ))

prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)])


# retriever
retriever = lc_client.as_retriever(search_kwargs={"k": 2})
tool = create_retriever_tool(
    retriever, 
    "search_geologic_data",
    "Searches and returns documents regarding geological features, entities and concepts."
)
tools = [tool]


# agent
agent = OpenAIFunctionsAgent(llm=llm,
                             tools=tools,
                             prompt=prompt)

agent_stream = OpenAIFunctionsAgent(llm=llm_stream,
                                    tools=tools,
                                    prompt=prompt)

# runnable chain
# return_intermediate_steps needs to be True! otherwise a keyError happens in `agent_token_buffer_memory.py`
chain = AgentExecutor(agent=agent,
                      tools=tools, 
                      memory=memory,
                      verbose=verbose_mode,
                      return_intermediate_steps=True)

chain_stream = AgentExecutor(agent=agent_stream,
                             tools=tools, 
                             memory=memory_stream,
                             verbose=verbose_mode,
                             return_intermediate_steps=True)
