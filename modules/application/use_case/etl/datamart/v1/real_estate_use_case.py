import os

from modules.adapter.infrastructure.etl.mart_real_estates import TransformRealEstate
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    BasicInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.real_estate_model import (
    RealEstateModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.basic_info_model import (
    BasicInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)
from datetime import date

from modules.adapter.infrastructure.sqlalchemy.repository.real_estate_repository import (
    SyncRealEstateRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BaseRealEstateUseCase:
    def __init__(
        self,
        topic: str,
        basic_repo: SyncBasicRepository,
        real_estate_repo: SyncRealEstateRepository,
    ):
        self._topic: str = topic
        self._basic_repo: SyncBasicRepository = basic_repo
        self._real_estate_repo: SyncRealEstateRepository = real_estate_repo
        self._transfer: TransformRealEstate = TransformRealEstate()

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"


class RealEstateUseCase(BaseRealEstateUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        """
        1. real_estates.id ==  place_id
        2. place_id가 없는 경우 mart로 etl 하지 않음 (의미가 없기 때문에)
        """
        today = date.today()

        # 단지 기본 정보
        basic_infos: list[BasicInfoEntity] | None = self._basic_repo.find_by_date(
            target_model=BasicInfoModel, target_date=today
        )
        results: list[RealEstateModel] | None = self._transfer.start_etl(
            from_model="basic_infos", target_list=basic_infos
        )

        if results:
            self.__upsert_to_warehouse(results=results)

    """
    insert, update
    """

    def __upsert_to_warehouse(
        self,
        results: list[RealEstateModel],
    ) -> None:
        for result in results:
            exists_result: bool = self._real_estate_repo.exists_by_key(value=result)

            if not exists_result:
                # insert
                self._real_estate_repo.save(value=result)
            else:
                # update
                self._real_estate_repo.update(value=result)
