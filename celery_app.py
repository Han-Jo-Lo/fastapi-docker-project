from celery import Celery

app_celery=Celery(
    'worker',
    backend='redis://redis:6379/1',
    broker='redis://redis:6379/2',
    include=['tasks']
)
