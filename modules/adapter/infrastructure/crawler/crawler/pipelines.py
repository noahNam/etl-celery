from scrapy import Spider

from modules.adapter.infrastructure.crawler.crawler.items import (
    KaptAreaInfoItem,
    KaptLocationInfoItem,
    LegalDongCodeItem,
    GovtBldTopInfoItem,
    GovtBldMidInfoItem,
    GovtBldAreaInfoItem,
)
from modules.adapter.infrastructure.sqlalchemy.database import db
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_bld_area_info_model import (
    GovtBldAreaInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_bld_middle_info_model import (
    GovtBldMiddleInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_bld_top_info_model import (
    GovtBldTopInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_area_info_model import (
    KaptAreaInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_location_info_model import (
    KaptLocationInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.legal_dong_code_model import (
    LegalDongCodeModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.govt_bld_repository import (
    SyncGovtBldRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.legal_dong_code_repository import (
    SyncLegalDongCodeRepository,
)


class KaptPipeline:
    def __init__(self):
        self._repo: SyncKaptRepository = SyncKaptRepository(session_factory=db.session)

    def process_item(
        self, item: KaptAreaInfoItem | KaptLocationInfoItem, spider: Spider
    ):
        """spider parameter: 사용하지 않지만 남겨두어야 제대로 작동합니다."""
        new_model = None
        if isinstance(item, KaptAreaInfoItem):
            new_model = KaptAreaInfoModel(**item.dict())
        elif isinstance(item, KaptLocationInfoItem):
            new_model = KaptLocationInfoModel(**item.dict())

        if not self._repo.is_exists_by_kapt_code(new_model):
            self._repo.save(new_model)

        return item


class LegalCodePipeline:
    def __init__(self):
        self._repo: SyncLegalDongCodeRepository = SyncLegalDongCodeRepository(
            session_factory=db.session
        )

    def process_item(self, item: LegalDongCodeItem, spider: Spider):
        """spider parameter: 사용하지 않지만 남겨두어야 제대로 작동합니다."""
        new_model: LegalDongCodeModel | None = LegalDongCodeModel(**item.dict())

        if not self._repo.is_exists_by_legal_codes(legal_code_orm=new_model):
            self._repo.save(new_model)

        return item


class GovtBldPipeline:
    def __init__(self):
        self._repo: SyncGovtBldRepository = SyncGovtBldRepository(
            session_factory=db.session
        )

    def process_item(
        self,
        item: GovtBldTopInfoItem | GovtBldMidInfoItem | GovtBldAreaInfoItem,
        spider: Spider,
    ):
        new_model = None

        if isinstance(item, GovtBldTopInfoItem):
            new_model = GovtBldTopInfoModel(**item.dict())
        elif isinstance(item, GovtBldMidInfoItem):
            new_model = GovtBldMiddleInfoModel(**item.dict())
        elif isinstance(item, GovtBldAreaInfoItem):
            new_model = GovtBldAreaInfoModel(**item.dict())

        if new_model:
            if not self._repo.is_exists(new_model):
                self._repo.save(new_model)

        return item
