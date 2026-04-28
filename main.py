#cd "/home/hanjo/Documents/Python Scripts/FastAPI/05-redis_como_memoria_persistente/"
#uvicorn main:app --reload
#Se debe hacer lo anterior puesto que el archivo main no se encuentra en el 
# directorio actual, sino en el directorio 05-redis_como_memoria_persistente
#tambien se debe correr el worker en celery con el siguiente comando:
## celery -A celery_app:app_celery worker --loglevel=info

from fastapi import FastAPI
from celery_app import app_celery
from tasks import run_llm_graph
from celery.result import AsyncResult
from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id:str
    message:str

app=FastAPI()

@app.post('/chat')
async def chat(request:ChatRequest):
    task=run_llm_graph.delay(request.user_id,request.message)
    return{
        'task_id':task.id,
        'status':'queued'
    }
    

@app.get('/result/{task_id}')
def result(task_id:str):
    result=AsyncResult(task_id,app=app_celery)
    return{
        'status':result.status,
        'result':result.result
    }