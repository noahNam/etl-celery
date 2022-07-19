from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.bld_mapping_result_model import (
    BldMappingResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.apt_deal_kakao_history_model import (
    AptDealKakaoHistoryModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncBldMappingResultRepository:
    def save_all(
        self,
        bld_mapping_results: list[BldMappingResultModel] | None,
        apt_deal_kakao_histories: list[AptDealKakaoHistoryModel],
    ) -> None:
        if not bld_mapping_results and not apt_deal_kakao_histories:
            return None

        try:
            session.add_all(bld_mapping_results)
            session.add_all(apt_deal_kakao_histories)
            session.commit()

        except Exception as e:
            logger.error(
                f"[SyncBldMappingResultsRepository][save_all] updated_at : "
                f"{bld_mapping_results[0].updated_at} error : {e}"
            )
            session.rollback()
            raise Exception
