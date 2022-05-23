from asyncio import (
    new_event_loop,
    set_event_loop,
)

from modules.adapter.infrastructure.crawler.crawler.items import (
    KaptAreaInfoItem,
    KaptLocationInfoItem,
)
from modules.adapter.infrastructure.sqlalchemy.database import db
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_area_info_model import (
    KaptAreaInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_location_info_model import (
    KaptLocationInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)


class KaptPipeline:
    def __init__(self):
        self._repo: SyncKaptRepository = SyncKaptRepository(session_factory=db.session)
        self._collected_area_infos: list[KaptAreaInfoItem] = list()
        self._collected_location_infos: list[KaptLocationInfoItem] = list()
        self._loop = new_event_loop()

    def process_item(self, item, spider):
        new_model = None
        if isinstance(item, KaptAreaInfoItem):
            new_model = KaptAreaInfoModel(**item.dict())
        elif isinstance(item, KaptLocationInfoItem):
            new_model = KaptLocationInfoModel(**item.dict())

        if not self._repo.exists_by_kapt_code(new_model):
            self._repo.save(new_model)

        return item
