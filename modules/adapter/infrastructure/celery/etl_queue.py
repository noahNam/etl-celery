from celery import Celery

from modules.adapter.infrastructure.message.broker.redis import redis
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
        include=["modules.adapter.presentation.cli.etl_tasks"],
        task_acks_late=True
    )
    app.conf.task_routes = {
        "modules.adapter.presentation.cli.etl_tasks.*": {
            "queue": "etl"
        }
    }

    init_broker()
    init_db()

    return app


etl_celery: Celery = make_celery(fastapi_config)


@etl_celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    pass



# celery -A modules.adapter.infrastructure.celery.etl_queue.celery flower --address=localhost --port=5555
# celery -A modules.adapter.infrastructure.celery.etl_queue.celery worker -B --loglevel=info -P threads -c 1
