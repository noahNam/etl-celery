from asyncio import run
from functools import wraps

from billiard.context import Process
from scrapy.settings import Settings

from modules.adapter.infrastructure.cache.redis import redis
from modules.adapter.infrastructure.celery.task_queue import celery
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import AsyncKaptRepository
from modules.adapter.presentation.cli.enum import TopicEnum
from modules.application.test_worker.v1.set_redis import SetRedisUseCase
from tests.unit.modules.application.use_case.kapt.v1.kapt_use_case import KaptOpenApiUseCase


def async_run(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return run(f(*args, **kwargs))
    return wrapper


async def get_task(topic: str):
    # if topic == TopicEnum.SET_REDIS.value:
    #     return SetRedisUseCase()
    if topic == TopicEnum.CRAWL_KAPT.value:
        return KaptOpenApiUseCase(
            topic=topic, cache=redis, kapt_repo=AsyncKaptRepository
        )


@celery.task
@async_run
async def start_worker(topic):
    uc = await get_task(topic=topic)
    await uc.execute()
    process = Process(target=uc.run_crawling)
    process.start()
    process.join()
