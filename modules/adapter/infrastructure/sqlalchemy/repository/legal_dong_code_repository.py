from sqlalchemy import exc, select

from core.domain.datalake.legal_dong_code.interface.legal_dong_code_repository import (
    LegalDongCodeRepository,
)
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.legal_dong_code_model import (
    LegalDongCodeModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncLegalDongCodeRepository(LegalDongCodeRepository):
    def find_by_id(self, legal_dong_code_id: int) -> LegalDongCodeEntity | None:
        legal_code_info = session.get(LegalDongCodeModel, legal_dong_code_id)

        if not legal_code_info:
            return None

        return legal_code_info.to_entity()

    def save(self, legal_dong_code_orm: LegalDongCodeModel | None) -> None:
        if not legal_dong_code_orm:
            return None
        try:
            session.add(legal_dong_code_orm)
            session.commit()
        except exc.IntegrityError as e:
            logger.error(
                f"[SyncLegalDongCodeRepository][save] id : {legal_dong_code_orm.id} error : {e}"
            )
            session.rollback()
            raise NotUniqueErrorException

    def is_exists_by_legal_codes(
        self, legal_code_orm: LegalDongCodeModel | None
    ) -> bool:
        result = None
        if legal_code_orm:
            query = (
                select(LegalDongCodeModel)
                .filter_by(
                    region_cd=legal_code_orm.region_cd,
                    sido_cd=legal_code_orm.sido_cd,
                    sgg_cd=legal_code_orm.sgg_cd,
                    umd_cd=legal_code_orm.umd_cd,
                    ri_cd=legal_code_orm.ri_cd,
                )
                .limit(1)
            )
            result = session.execute(query).scalars().first()

        if result:
            return True
        return False

    def find_all(self) -> list[LegalDongCodeEntity]:
        queryset = session.execute(select(LegalDongCodeModel)).scalars().all()

        if not queryset:
            return list()

        return [query.to_entity() for query in queryset]
