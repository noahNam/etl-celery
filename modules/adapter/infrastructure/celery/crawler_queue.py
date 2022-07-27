from celery import Celery
from celery.schedules import crontab

from modules.adapter.infrastructure.fastapi.config import Config, fastapi_config
from modules.adapter.infrastructure.message.broker.redis import redis
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
        include=["modules.adapter.presentation.cli.crawler_tasks"],
    )
    init_broker()
    init_db()

    return app


crawler_celery: Celery = make_celery(fastapi_config)


@crawler_celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from modules.adapter.presentation.cli import crawler_tasks

    # sender.add_periodic_task(
    #     10.0,
    #     tasks.start_crawler.s(topic=TopicEnum.CRAWL_KAPT.value),
    #     name='warehouse',
    # )

    # crawler_tasks.start_crawler.apply_async(kwargs={"topic": TopicEnum.CRAWL_KAPT.value})
    sender.add_periodic_task(
        crontab(hour=19, minute=00),
        kwargs={"topic": TopicEnum.CRAWL_APPLY_HOME.value},
    )

# celery -A modules.adapter.infrastructure.celery.crawler_queue.crawler_celery flower --address=localhost --port=5555
# celery -A modules.adapter.infrastructure.celery.crawler_queue.crawler_celery worker -B --loglevel=info -P threads -c 3
