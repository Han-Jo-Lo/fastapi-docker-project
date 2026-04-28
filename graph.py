from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv
from typing import Annotated
load_dotenv()

llm=ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0,
    max_tokens=200,
)

class State(TypedDict):
    messages:Annotated[list,add_messages]

def chat_node(state:State):
    messages=state['messages']
    response=llm.invoke(messages)
    return {'messages':response}

builder=StateGraph(State)
builder.add_node('chat',chat_node)
builder.add_edge(START,'chat')
builder.add_edge('chat',END)

Graph=builder.compile()