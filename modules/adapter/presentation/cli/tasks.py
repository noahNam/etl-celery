from modules.adapter.infrastructure.celery.task_queue import celery
from modules.adapter.presentation.cli.enum import TopicEnum
from modules.application.test_worker.v1.set_redis import SetRedisUseCase


def get_task(topic: str):
    if topic == TopicEnum.SET_REDIS.value:
        return SetRedisUseCase()


@celery.task
def start_worker(topic):
    us = get_task(topic=topic)
    us.execute()
