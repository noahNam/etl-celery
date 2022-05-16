from typing import Callable, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.kapt.interface.kapt_repository import KaptRepository
from modules.adapter.infrastructure.sqlalchemy.repository import BaseAsyncRepository
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class AsyncKaptRepository(KaptRepository, BaseAsyncRepository):
    def __init__(
        self, session_factory: Callable[..., AsyncContextManager[AsyncSession]]
    ):
        super().__init__(session_factory=session_factory)

    async def find_by_id(self, house_id: int):
        print("find_by_id")
