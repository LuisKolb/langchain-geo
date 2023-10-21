from dotenv import load_dotenv
import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from langchain.schema.messages import SystemMessage
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.prompts import MessagesPlaceholder
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents import AgentExecutor

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


from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature = 0)


# This is needed for both the memory and the prompt
memory_key = "luis"
memory = AgentTokenBufferMemory(memory_key=memory_key, llm=llm)



system_message = SystemMessage(
        content=(
            "Do your best to answer the questions. "
            "You must use the tools available to look up relevant information, if neccessary. "
            "If you use the tools, make sure to always return the URL in addition to the response."
        )
)
prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)]
    )


retriever = lc_client.as_retriever(search_kwargs={"k": 2})
tool = create_retriever_tool(
    retriever, 
    "search_geologic_data",
    "Searches and returns documents regarding geological features, entities and concepts."
)
tools = [tool]


agent = OpenAIFunctionsAgent(llm=llm,
                             tools=tools,
                             prompt=prompt)


# TODO: fix the below behaviour 
# return_intermediate_steps is True because langcorn uses `chain.output_keys > 1` to identify the return data model...
chain = AgentExecutor(agent=agent,
                      tools=tools, 
                      memory=memory,
                      verbose=True,
                      return_intermediate_steps=True)
