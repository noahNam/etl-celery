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
    )
    init_broker()
    init_db()

    return app


etl_celery: Celery = make_celery(fastapi_config)


@etl_celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from modules.adapter.presentation.cli import etl_tasks

    # sender.add_periodic_task(
    #     10.0,
    #     etl_tasks.start_worker.s(topic=TopicEnum.ETL_WH_BASIC_INFOS.value),
    #     name=TopicEnum.ETL_WH_BASIC_INFOS.value,
    # )
    # etl_tasks.start_worker.delay(topic=TopicEnum.ETL_WH_BASIC_INFOS.value)
    # etl_tasks.start_worker.delay(topic=TopicEnum.ETL_DL_SUBS_INFOS.value)
    etl_tasks.start_worker.delay(topic=TopicEnum.ETL_WH_SUBS_INFOS.value)
    # etl_tasks.start_worker.delay(topic=TopicEnum.ETL_MART_REAL_ESTATES.value)
    # etl_tasks.start_worker.delay(topic=TopicEnum.ETL_MART_PRIVATE_SALES.value)
    # etl_tasks.start_worker.delay(topic=TopicEnum.ETL_MART_DONG_TYPE_INFOS.value)
    # etl_tasks.start_worker.delay(topic=TopicEnum.ETL_MART_PRIVATE_SALE_DETAILS.value)

    # etl_tasks.start_worker.apply_async(kwargs={"topic": TopicEnum.CRAWL_KAPT.value})
    # etl_tasks.start_worker.apply_async(kwargs={"topic": TopicEnum.CRAWL_KAKAO_API.value})
    # etl_tasks.start_worker.apply_async(
    #     kwargs={"topic": TopicEnum.CRAWL_LEGAL_DONG_CODE.value}
    # )
    # etl_tasks.start_worker.apply_async(
    #     kwargs={"topic": TopicEnum.CRAWL_BUILDING_MANAGE.value}
    # )

    # DL 아파트 실거래가 매핑테이블
    # etl_tasks.start_worker.delay(topic=TopicEnum.ETL_DL_BLD_MAPPING_RESULTS.value)  # 실거래가, kapt, kakao데이터 수집 이후

    # DW 아파트 실거래가
    # etl_tasks.start_worker.delay(topic=TopicEnum.ETL_WH_APT_DEALS.value)  # 매핑테이블 이후, 건축물대장 업데이트 이후
    # etl_tasks.start_worker.delay(topic=TopicEnum.ETL_WH_APT_RENTS.value)
    # etl_tasks.start_worker.delay(topic=TopicEnum.ETL_WH_OFCTL_DEALS.value)
    # etl_tasks.start_worker.delay(topic=TopicEnum.ETL_WH_OFCTL_RENTS.value)
    # etl_tasks.start_worker.delay(topic=TopicEnum.ETL_WH_RIGHT_LOG_OUTS.value)
    #
    # etl_tasks.start_worker.delay(topic=TopicEnum.ETL_WH_UPDATE_SUPPLY_AREA.value)  # 실거래가 이후, 건축물대장 이후

    etl_tasks.start_worker.delay(topic=TopicEnum.ETL_MART_PUBLIC_SALES.value)


# celery -A modules.adapter.infrastructure.celery.etl_queue.celery flower --address=localhost --port=5555
# celery -A modules.adapter.infrastructure.celery.etl_queue.celery worker -B --loglevel=info -P threads -c 1
