from sqlalchemy import exc, select

from core.domain.datalake.kakao_api.interface.kakao_api_result_repository import (
    KakaoApiRepository,
)
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kakao_api_result_entity import (
    KakaoApiResultEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kakao_api_result_model import (
    KakaoApiResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository import BaseSyncRepository
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncKakaoApiRepository(BaseSyncRepository, KakaoApiRepository):
    def find_by_id(self, house_id: int) -> KakaoApiResultEntity | None:
        with self.session_factory() as session:
            kakao_info = session.get(KakaoApiResultModel, house_id)

        if not kakao_info:
            return None

        return kakao_info.to_entity()

    def save(self, kakao_orm: KakaoApiResultModel | None) -> int | None:
        if not kakao_orm:
            return None
        with self.session_factory() as session:
            try:
                session.add(kakao_orm)
                session.commit()
            except exc.IntegrityError as e:
                logger.error(
                    f"[SyncKakaoApiRepository][save] jibun_address : {kakao_orm.jibun_address} error : {e}"
                )
                session.rollback()
                raise NotUniqueErrorException

            # find pk
            saved_orm = (
                session.execute(
                    select(KakaoApiResultModel).filter_by(
                        jibun_address=kakao_orm.jibun_address,
                        bld_name=kakao_orm.bld_name,
                    )
                )
                .scalars()
                .first()
            )

            if saved_orm:
                return saved_orm.id
        return None
