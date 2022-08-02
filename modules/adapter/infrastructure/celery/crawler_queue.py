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
        include=["modules.adapter.presentation.cli.crawler_tasks", "modules.adapter.presentation.cli.etl_tasks"],

    )
    app.conf.task_routes = {
        "modules.adapter.presentation.cli.crawler_tasks.*": {
            "queue": "crawler"
        },
        "modules.adapter.presentation.cli.etl_tasks.*": {
            "queue": "etl"
        },
        "app.commands.tasks.*": {
            "queue": "tanos"
        },
    }

    init_broker()
    init_db()

    return app


crawler_celery: Celery = make_celery(fastapi_config)


@crawler_celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from modules.adapter.presentation.cli import crawler_tasks
    from modules.adapter.presentation.cli import etl_tasks

    # crawler_tasks.start_crawler.apply_async(kwargs={"topic": TopicEnum.CRAWL_KAPT.value})
    sender.add_periodic_task(
        schedule=crontab(hour=19, minute=5),
        sig=crawler_tasks.start_crawler.s(topic=TopicEnum.CRAWL_APPLY_HOME.value),
        name="datalake_apply_home",
        queue="crawler"
    )

    sender.add_periodic_task(
        schedule=crontab(hour=19, minute=15),
        sig=etl_tasks.start_worker.s(topic=TopicEnum.ETL_WH_BASIC_INFOS.value),
        name="warehouse_basic_infos",
        queue="etl"
    )

# celery -A modules.adapter.infrastructure.celery.crawler_queue.crawler_celery flower --address=localhost --port=5555
# celery -A modules.adapter.infrastructure.celery.crawler_queue.crawler_celery worker -B --loglevel=info -P threads -c 3
