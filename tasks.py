from graph import Graph
from memory import save_memory,load_memory
from celery_app import app_celery
from langchain_core.messages import HumanMessage,AIMessage

@app_celery.task
def run_llm_graph(user_id:str,message:str):
    history=load_memory(user_id)
    langgraph_messages=[]
    for msg in history:
        if msg['role']=='user':
            langgraph_messages.append(HumanMessage(history['messages']))
        else:
            langgraph_messages.append(AIMessage(history['messages']))
    langgraph_messages.append(HumanMessage(message))

    response=Graph.invoke(
        {'messages':langgraph_messages}
    )

    updated_messages=response['messages']
    last_message=updated_messages[-1].content

    serialized_messages=[]

    for msg in updated_messages:
        if isinstance(msg,HumanMessage):
            serialized_messages.append(
                {'role':'user',
                'messages':msg.content}
            )
        else:
            serialized_messages.append(
                {'role':'assistant',
                'messages':msg.content}
            )
    
    save_memory(user_id,serialized_messages)

    return last_message