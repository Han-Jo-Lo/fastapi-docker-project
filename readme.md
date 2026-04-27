# LLM + FastAPI + Redis + Celery + Docker

Integracion de un LLM basico con FastAPI utilizando Redis para el manejo de memoria y Celery para el manejo de las tareas de forma asincrona lista para ser contenirizada

---

## Descripcion

### Este proyecto muestra como se conecta un LLM con FastAPI, en donde se utiliza LangGraph el cual solo tiene un nodo, y retorna la salida del LLM, el flujo es el siguiente:

1. Atraves de un Endpoint se envia un texto/conversación para que el LLM lo procese
2. Esta conversación es tomada por Celery y encolada en el Broker (Redis)
3. Celery a traves del worker revisa que trabajos (en este caso conversaciones) hay encoladas para ejecutar la tarea
4. Celery toma la tarea y la ejecuta
5. **Recuperación de Contexto (Persistencia):** Se recupera el historial de mensajes desde **Redis**, el cual actúa como nuestro almacén de persistencia. Para optimizar el rendimiento y el contexto del modelo, se cargan únicamente las últimas 10 interacciones.
6. **Orquestación de Memoria:** Se recupera el historial de Redis, se serializa al formato de LangChain (`HumanMessage`/`AIMessage`) y se inyecta en el estado del grafo".
7. Se Ejecuta el flujo de LangGraph
8. **Persistencia de la Respuesta:** Una vez que el grafo de LangGraph devuelve una respuesta, esta se serializa y se guarda nuevamente en **Redis**. Esto asegura que la memoria de la conversación se mantenga actualizada para futuras peticiones del mismo usuario.
9. **Consulta Asíncrona de Resultados:** Debido a que la tarea se ejecuta en segundo plano (worker de Celery), el usuario no recibe la respuesta de inmediato. En su lugar, debe utilizar el `task_id` devuelto inicialmente para consultar el estado y el contenido final a través del endpoint `/result/{task_id}`.
10. Todo el proyecto esta contenirizado para que pueda ser ejecutadoen otro ambiente

---

## Tecnologias utilizadas

1. Python
2. FastAPI
3. Celery
4. Redis

- DB 0: Almacén de persistencia para la memoria de chat (historial de mensajes).
- DB 1: Backend de resultados para Celery.
- DB 2: Broker de mensajería para la gestión de colas de tareas.

1. LangGraph
2. Docker

---

## Instalacion y configuracion

### 1. Clonar el repositorio

> `git clone https://github.com/Han-Jo-Lo/fastapi-docker-project.git`

### 2. dependiendo como se quiera ejecutar el codigo hay dos formas de realizar este proceso

```
a. Con Docker
    1. Abrimos la terminal y nos dirigimos hasta la carpeta del proyecto
    2. Se debe crear el archio .env el cual se encarga de guardar las variables de entorno en este caso
        OPENAI_API_KEY=tu_clave_aqui
    3. Construimos el proyecto de Docker
        docker-compose up --build
    4. En el navegador nos dirigimos al swager de FastAPI http:localhost:8000/docs
b. Ejecutando en un entorno de programación
    1. Se instala Redis
        sudo apt install redis-server (Ubuntu)
    2. Abrir el proyecto en su IDE de preferencia (ej. VS Code)
    3. Se debe crear el archio .env el cual se encarga de guardar las variables de entorno en este caso
        OPENAI_API_KEY=tu_clave_aqui
    4. Se abre una terminal
    5. Se recomienda crear un entorno virtual
    6. Se cambia el directoria hasta la carpeta del proyecto
    7. Se instalan las dependecias
        pip install -r requirements.txt
    8. Se ejecuta FastAppi por medio uvicorn
        uvicorn main:app --reload
    9. Se abre otra terminal y se ejecuta el worker de Celery
        celery -A celery_app:app_celery worker --loglevel=info
    10. En el navegador nos dirigimos al swager de FastAPI http:localhost:8000/docs
```

---

### Autor 👤

- Hans - [LinkedIn](https://www.linkedin.com/in/hans-echeverri/)

