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

app=FastAPI()

@app.post('/chat')
async def chat(user_id:str,message:str):
    task=run_llm_graph.delay(user_id,message)
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