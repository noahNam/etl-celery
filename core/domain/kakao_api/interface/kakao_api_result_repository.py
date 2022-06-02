from abc import ABC, abstractmethod

from modules.adapter.infrastructure.sqlalchemy.entity.v1.kakao_api_result_entity import (
    KakaoApiResultEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kakao_api_result_model import (
    KakaoApiResultModel,
)


class KakaoApiRepository(ABC):
    @abstractmethod
    def find_by_id(self, house_id: int) -> KakaoApiResultEntity | None:
        pass

    @abstractmethod
    def save(self, kakao_orm: KakaoApiResultModel | None) -> None:
        pass
