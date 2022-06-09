from celery import Celery

from modules.adapter.infrastructure.cache.redis import redis
from modules.adapter.infrastructure.fastapi.config import Config, fastapi_config
from modules.adapter.infrastructure.sqlalchemy.database import db
from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.adapter.presentation.cli.enum import TopicEnum

logger = logger_.getLogger(__name__)


def init_broker():
    redis.connect()
    if redis.is_available():
        logger.info("Redis is ready")


def init_db():
    db.create_all()
    logger.info("Database is ready")


def make_celery(app_config: Config):
    app: Celery = Celery(
        "celery",
        backend=app_config.BACKEND_RESULT,
        broker=app_config.REDIS_URL,
        timezone=app_config.TIMEZONE,
        enable_utc=app_config.CELERY_ENABLE_UTC,
        include=["modules.adapter.presentation.cli.tasks"],
    )
    init_broker()
    init_db()

    return app


celery: Celery = make_celery(fastapi_config)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from modules.adapter.presentation.cli import tasks

    # sender.add_periodic_task(
    #     10.0,
    #     tasks.start_worker.s(topic=TopicEnum.CRAWL_KAPT.value),
    #     name='kapt',
    # )

    # tasks.start_worker.apply_async(kwargs={"topic": TopicEnum.CRAWL_KAPT.value})
    # tasks.start_worker.apply_async(kwargs={"topic": TopicEnum.CRAWL_KAKAO_API.value})
    # tasks.start_worker.apply_async(
    #     kwargs={"topic": TopicEnum.CRAWL_LEGAL_DONG_CODE.value}
    # )
    tasks.start_worker.apply_async(
        kwargs={"topic": TopicEnum.CRAWL_BUILDING_MANAGE.value}
    )


# celery -A modules.adapter.infrastructure.celery.task_queue.celery flower --address=localhost --port=5555
# celery -A modules.adapter.infrastructure.celery.task_queue.celery worker -B --loglevel=info -P threads -c 3
