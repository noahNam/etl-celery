from pubsub import pub

from modules.adapter.infrastructure.pypubsub.enum.call_failure_history_enum import (
    CallFailureTopicEnum,
)
from modules.adapter.infrastructure.sqlalchemy.database import db
from modules.adapter.infrastructure.sqlalchemy.repository.call_failure_history_repository import (
    SyncFailureRepository,
)


def save_crawling_failure(fail_orm) -> None:
    SyncFailureRepository(db.session).save(fail_orm=fail_orm)


pub.subscribe(save_crawling_failure, CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value)
