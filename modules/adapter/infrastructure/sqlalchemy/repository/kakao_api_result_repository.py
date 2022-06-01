from core.domain.kakao_api.interface.kakao_api_result_repository import (
    KakaoApiRepository,
)
from modules.adapter.infrastructure.sqlalchemy.entity.v1.kakao_api_result_entity import (
    KakaoApiResultEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kakao_api_result_model import (
    KakaoApiResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository import BaseSyncRepository


class SyncKakaoApiRepository(BaseSyncRepository, KakaoApiRepository):
    def find_by_id(self, house_id: int) -> KakaoApiResultEntity | None:
        with self.session_factory() as session:
            kakao_info = session.get(KakaoApiResultModel, house_id)

        if not kakao_info:
            return None

        return kakao_info.to_entity()

    def save(self, kakao_orm: KakaoApiResultModel | None) -> None:
        pass

    def exists_by_id(self, kakao_orm: KakaoApiResultModel | None) -> bool:
        pass
