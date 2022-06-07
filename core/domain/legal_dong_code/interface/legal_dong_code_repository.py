from abc import ABC, abstractmethod

from modules.adapter.infrastructure.sqlalchemy.entity.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.legal_dong_code_model import (
    LegalDongCodeModel,
)


class LegalDongCodeRepository(ABC):
    @abstractmethod
    def find_by_id(self, legal_dong_code_id: int) -> LegalDongCodeEntity | None:
        pass

    @abstractmethod
    def save(self, legal_dong_code_orm: LegalDongCodeModel | None) -> None:
        pass
