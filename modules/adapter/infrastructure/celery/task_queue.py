from celery import Celery

from modules.adapter.infrastructure.fastapi.config import Config, fastapi_config
from modules.adapter.presentation.cli.enum import TopicEnum


def make_celery(app_config: Config):
    app: Celery = Celery(
        "celery",
        backend=app_config.BACKEND_RESULT,
        broker=app_config.REDIS_URL,
        timezone=app_config.TIMEZONE,
        enable_utc=app_config.CELERY_ENABLE_UTC,
        include=["modules.adapter.presentation.cli.tasks"],
    )

    return app


celery: Celery = make_celery(fastapi_config)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from modules.adapter.presentation.cli import tasks

    # sender.add_periodic_task(
    #     20.0,
    #     tasks.start_worker.s(topic=TopicEnum.SET_REDIS.value),
    #     name='set-redis',
    # )

    tasks.start_worker.delay(topic=TopicEnum.SET_REDIS.value)


# celery -A modules.adapter.infrastructure.celery.task_queue.celery flower --address=localhost --port=5555
# celery -A modules.adapter.infrastructure.celery.task_queue.celery worker -B --loglevel=info -P threads -c 3
