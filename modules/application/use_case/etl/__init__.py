import os
from typing import Any

from modules.adapter.infrastructure.pypubsub.enum.call_failure_history_enum import (
    CallFailureTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.event_listener import event_listener_dict
from modules.adapter.infrastructure.pypubsub.event_observer import send_message
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.call_failure_history_model import (
    CallFailureHistoryModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BaseETLUseCase:
    def __init__(
        self,
        topic: str,
    ):
        self._topic: str = topic

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"

    def execute(self):
        """각 UseCase마다 직접 구현"""
        pass

    def _save_crawling_failure(
        self,
        failure_value: Any,
        ref_table: str,
        param: Any | None,
        reason: Exception,
    ) -> None:
        fail_orm: CallFailureHistoryModel = CallFailureHistoryModel(
            ref_id=failure_value,
            ref_table=ref_table,
            param=param,
            reason=reason,
            is_solved=False,
        )

        send_message(
            topic_name=CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value,
            fail_orm=fail_orm,
        )
        event_listener_dict.get(
            f"{CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value}", None
        )
