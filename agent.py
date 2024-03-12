from re import template
from chainlit import user
import langchain
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from langchain.tools import retriever
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain import hub
from langchain.chains import LLMChain
from ingest import load_vec_db, refresh_db
import openai
import os
from typing import Optional, List
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from typing import Optional, List
import pandas as pd


openai.api_key=os.getenv("OPENAI_API_KEY")

prompt = hub.pull("zulqarnain/openai-functions-agent_appoint")

# to create a tool 
def create_tools(retrivar):
  retriever_tool=create_retriever_tool(retriever=retrivar,name="booked_appointment_data",description="the data about those persone who booked their appointments",
                                       document_prompt="you seek the booked appointment in the data")
  return [retriever_tool]
#################################################################################################
def create_agent_with_exe():
  # load the agents!
 
  llm = ChatOpenAI(temperature=0)
  retriever=load_vec_db()
  tools=create_tools(retriever)
  agent = create_openai_functions_agent(llm, tools,prompt)
  executor = AgentExecutor(agent=agent,tools=tools)
  return executor


executor=create_agent_with_exe()



chat_history=[]
#####################################################################################
def generate_response(query:str):
  # Here we pass in an empty list of messages for chat_history because it is the first message in the chat
    res=executor.invoke({"input": query, "chat_history": chat_history})
    chat_history.append(HumanMessage(content=query))
    chat_history.append(AIMessage(content=res["output"]))

    return res["output"]

###########################################################################################
import pandas as pd

def insert_data_to_dataframe(data):
    df=pd.read_csv("database.csv")
    """
    Insert a list of data as a new row in the given data frame.

    Args:
        data (list): A list of data to insert as a new row. The list should have the same length as the number of columns in the data frame.
        df (pandas.DataFrame): The data frame to insert the data into.

    Returns:
        None
    """
    new_row = pd.DataFrame([data], columns=df.columns)
    df = df.append(new_row, ignore_index=True)
    df.to_csv("database.csv",index=False)
    print(f"inserted_data:{data}")


#######################
import ast
def extract_data(chat_history):
  template = """
  you are a helpful chat history summarizer your task is to summarize the chat history and extract the information from the chat history like: Name appointment booker, date, time,phone email and return the extracted information in the foramt of python list for example ["name of appointment booker","date of appointment","time of appointment","phone number of appointment booker","email of appoitment booker"]   here is the history: {chat_history}
  """
  prompt_template = PromptTemplate(template=template,
                                   input_variables=["chat_history"])
  chain = LLMChain(llm=OpenAI(), prompt=prompt_template)
  res = chain.run(chat_history)
  
  res=ast.literal_eval(res)
  
  insert_data_to_dataframe(res)
  #refresh_db()  "here to refresh the database whcih is updated"
  return res


