import os
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BaseEtlUseCase:
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