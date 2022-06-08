import os

from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class KaptUseCase:
    def __init__(
        self,
        topic: str,
        kapt_repo: SyncKaptRepository,
    ):
        self._topic: str = topic
        self._repo: SyncKaptRepository = kapt_repo

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"


class KaptOpenApiUseCase(KaptUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        pass