from sqlalchemy import exc, select

from core.domain.datalake.kakao_api.interface.kakao_api_result_repository import (
    KakaoApiRepository,
)
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kakao_api_result_entity import (
    KakaoApiResultEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kakao_api_result_model import (
    KakaoApiResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_basic_info_model import (
    KaptBasicInfoModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kakao_api_result_entity import (
    KakaoApiAddrEntity,
)

logger = logger_.getLogger(__name__)


class SyncKakaoApiRepository(KakaoApiRepository):
    def find_by_id(self, id: int) -> KakaoApiResultEntity | None:
        kakao_info = session.get(KakaoApiResultModel, id)

        if not kakao_info:
            return None

        return kakao_info.to_entity()

    def save(self, kakao_orm: KakaoApiResultModel | None) -> int | None:
        if not kakao_orm:
            return None
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

    def is_exists_by_origin_address(
        self, kakao_orm: KakaoApiResultModel | None
    ) -> bool:
        result = None
        if kakao_orm:
            query = (
                select(KakaoApiResultModel)
                .filter_by(
                    origin_jibun_address=kakao_orm.origin_jibun_address,
                    origin_road_address=kakao_orm.origin_road_address,
                )
                .limit(1)
            )
            result = session.execute(query).scalars().first()

        if result:
            return True
        return False

    def find_all(self) -> list[KakaoApiAddrEntity]:
        query = (
            session.query(KakaoApiResultModel)
            .with_entities(
                KakaoApiResultModel.id,
                KakaoApiResultModel.road_address,
                KakaoApiResultModel.jibun_address,
                KakaoApiResultModel.bld_name,
                KaptBasicInfoModel.house_id,
            )
            .join(
                KaptBasicInfoModel,
                KakaoApiResultModel.id == KaptBasicInfoModel.place_id,
                isouter=True,
            )
            .where(KaptBasicInfoModel.house_id != None)
        )
        querysets = query.all()

        if not querysets:
            return list()
        else:
            return [
                self._to_entity_for_bld_mapping(queryset=queryset)
                for queryset in querysets
            ]

    def _to_entity_for_bld_mapping(self, queryset) -> KakaoApiAddrEntity:
        return KakaoApiAddrEntity(
            id=queryset.id,
            house_id=queryset.house_id,
            road_address=queryset.road_address,
            jibun_address=queryset.jibun_address,
            bld_name=queryset.bld_name,
        )
