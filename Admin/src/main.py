from fastapi import FastAPI, Depends, Request
from celery import Celery
import os
from models.task import TemplateModel
from core.config import settings
from contextlib import asynccontextmanager
from fastapi.responses import ORJSONResponse, JSONResponse


@asynccontextmanager
async def custom_lifespan_context(app: FastAPI):
    # Настройка Celery
    app.celery_app = Celery('tasks', broker=os.environ.get('CELERY_BROKER_URL',
                                                           f'redis://{settings.redis.host}:{settings.redis.port}'))
    app.celery_app.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND',
                                                        f'redis://{settings.redis.host}:{settings.redis.port}')
    yield


app = FastAPI(
    lifespan=custom_lifespan_context,
    description="Notification logic",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


# Периодическая задача для рассылки сообщений
@app.celery_app.task
def send_periodic_email(data: TemplateModel):
    # отправлем в сервис нотификации
    print(f"Sending email \n{data.template}")

# Эндпоинт для создания периодической задачи


@app.post("/periodic-tasks")
async def create_periodic_task(task: TemplateModel, request: Request):
    # Проверка шаблона Jinja
    try:
        jinja_env = app.jinja_env
        template = jinja_env.from_string(task.template)
    except Exception as e:
        return {"error": f"Invalid Jinja template: {e}"}

    # Создание периодической задачи Celery
    send_periodic_email.delay(task)
    return task.template
