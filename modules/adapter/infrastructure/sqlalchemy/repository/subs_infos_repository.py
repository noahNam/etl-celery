from typing import Type

from sqlalchemy import exc, select, desc, update

from core.domain.datalake.subscription_info.interface.subscription_info_repository import (
    SubscriptionInfoRepository,
)
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.subs_entity import (
    ApplyHomeEntity,
    GoogleSheetApplyHomeEntity,
    SubscriptionInfoEntity,
    SubscriptionManualInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.applyhome_dl_model import (
    ApplyHomeModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.google_sheet_applyhome_dl_model import (
    GoogleSheetApplyHomeModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_info_model import (
    SubscriptionInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_manual_info_model import (
    SubscriptionManualInfoModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncSubscriptionInfoRepository(SubscriptionInfoRepository):
    def save_to_new_schema(
        self, value: SubscriptionInfoModel | SubscriptionManualInfoModel
    ) -> None:
        try:
            session.add(value)
            session.commit()
        except exc.IntegrityError as e:
            logger.error(
                f"[SyncSubscriptionInfoRepository][save_to_new_schema] target_model : {value} error : {e}"
            )
            session.rollback()
            raise NotUniqueErrorException

    def update_to_new_schema(
        self, value: SubscriptionInfoModel | SubscriptionManualInfoModel
    ) -> None:
        if isinstance(value, SubscriptionInfoModel):
            session.execute(
                update(SubscriptionInfoModel)
                .where(SubscriptionInfoModel.id == value.id)
                .values(
                    subs_id=value.subs_id,
                    offer_date=value.offer_date,
                    notice_winner_date=value.notice_winner_date,
                    name=value.name,
                    area_type=value.area_type,
                    supply_price=value.supply_price,
                    second_subs_amount=value.second_subs_amount,
                    origin_address=value.origin_address,
                    new_address=value.new_address,
                    supply_household=value.supply_household,
                    offer_notice_url=value.offer_notice_url,
                    move_in_date=value.move_in_date,
                    contract_date=value.contract_date,
                    hompage_url=value.hompage_url,
                    special_supply_date=value.special_supply_date,
                    special_supply_etc_date=value.special_supply_etc_date,
                    special_etc_gyeonggi_date=value.special_etc_gyeonggi_date,
                    first_supply_date=value.first_supply_date,
                    first_supply_etc_date=value.first_supply_etc_date,
                    first_etc_gyeonggi_date=value.first_etc_gyeonggi_date,
                    second_supply_date=value.second_supply_date,
                    second_supply_etc_date=value.second_supply_etc_date,
                    second_etc_gyeonggi_date=value.second_etc_gyeonggi_date,
                    supply_area=value.supply_area,
                    region=value.region,
                    housing_category=value.housing_category,
                    rent_type=value.rent_type,
                    construct_company=value.construct_company,
                    contact=value.contact,
                    subscription_date=value.subscription_date,
                    special_supply_status=value.special_supply_status,
                    cmptt_rank=value.cmptt_rank,
                    special_household=value.special_household,
                    multi_children_vol_etc_gyeonggi=value.multi_children_vol_etc_gyeonggi,
                    multi_children_vol_etc=value.multi_children_vol_etc,
                    multi_children_household=value.multi_children_household,
                    multi_children_vol=value.multi_children_vol,
                    newlywed_vol_etc_gyeonggi=value.newlywed_vol_etc_gyeonggi,
                    newlywed_vol_etc=value.newlywed_vol_etc,
                    newlywed_household=value.newlywed_household,
                    newlywed_vol=value.newlywed_vol,
                    first_life_vol_etc_gyeonggi=value.first_life_vol_etc_gyeonggi,
                    first_life_vol_etc=value.first_life_vol_etc,
                    first_life_household=value.first_life_household,
                    first_life_vol=value.first_life_vol,
                    old_parent_vol_etc_gyeonggi=value.old_parent_vol_etc_gyeonggi,
                    old_parent_vol_etc=value.old_parent_vol_etc,
                    old_parent_household=value.old_parent_household,
                    old_parent_vol=value.old_parent_vol,
                    agency_recommend_etc_gyeonggi=value.agency_recommend_etc_gyeonggi,
                    agency_recommend_etc=value.agency_recommend_etc,
                    agency_recommend_house_hold=value.agency_recommend_house_hold,
                    agency_recommend_vol=value.agency_recommend_vol,
                    official_general_household=value.official_general_household,
                    general_household=value.general_household,
                    first_accept_cnt=value.first_accept_cnt,
                    first_accept_cnt_gyeonggi=value.first_accept_cnt_gyeonggi,
                    first_accept_cnt_etc=value.first_accept_cnt_etc,
                    second_accept_cnt=value.second_accept_cnt,
                    second_accept_cnt_gyeonggi=value.second_accept_cnt_gyeonggi,
                    second_accept_cnt_etc=value.second_accept_cnt_etc,
                    first_cmptt_rate=value.first_cmptt_rate,
                    first_cmptt_rate_gyeonggi=value.first_cmptt_rate_gyeonggi,
                    first_cmptt_rate_etc=value.first_cmptt_rate_etc,
                    second_cmptt_rate=value.second_cmptt_rate,
                    second_cmptt_rate_gyeonggi=value.second_cmptt_rate_gyeonggi,
                    second_cmptt_rate_etc=value.second_cmptt_rate_etc,
                    lowest_win_point=value.lowest_win_point,
                    lowest_win_point_gyeonggi=value.lowest_win_point_gyeonggi,
                    lowest_win_point_etc=value.lowest_win_point_etc,
                    top_win_point=value.top_win_point,
                    top_win_point_gyeonggi=value.top_win_point_gyeonggi,
                    top_win_point_etc=value.top_win_point_etc,
                    avg_win_point=value.avg_win_point,
                    avg_win_point_gyeonggi=value.avg_win_point_gyeonggi,
                    avg_win_point_etc=value.avg_win_point_etc,
                    update_needed=value.update_needed,
                )
            )

        elif isinstance(value, SubscriptionManualInfoModel):
            session.execute(
                update(SubscriptionManualInfoModel)
                .where(SubscriptionManualInfoModel.id == value.id)
                .values(
                    subs_id=value.subs_id,
                    heat_type=value.heat_type,
                    vl_rat=value.vl_rat,
                    bc_rat=value.bc_rat,
                    hallway_type=value.hallway_type,
                    hhld_total_cnt=value.hhld_total_cnt,
                    park_total_cnt=value.park_total_cnt,
                    highest_floor=value.highest_floor,
                    dong_cnt=value.dong_cnt,
                    deposit=value.deposit,
                    middle_payment=value.middle_payment,
                    balance=value.balance,
                    restriction_sale=value.restriction_sale,
                    compulsory_residence=value.compulsory_residence,
                    bay=value.bay,
                    pansang_tower=value.pansang_tower,
                    kitchen_window=value.kitchen_window,
                    direct_window=value.direct_window,
                    alpha_room=value.alpha_room,
                    cyber_model_house_link=value.cyber_model_house_link,
                    supply_rate=value.supply_rate,
                    supply_rate_etc=value.supply_rate_etc,
                    update_needed=value.update_needed,
                )
            )

        session.commit()

    def find_all(
        self, target_model: Type[ApplyHomeModel | GoogleSheetApplyHomeModel]
    ) -> list[ApplyHomeEntity | GoogleSheetApplyHomeEntity] | None:
        queryset = (
            session.execute(select(target_model).order_by(desc(target_model.id)))
            .scalars()
            .all()
        )

        if not queryset:
            return None

        if target_model == GoogleSheetApplyHomeModel:
            return [query.to_google_sheet_apply_home_entity() for query in queryset]

        return [query.to_apply_home_entity() for query in queryset]

    def exists_by_key(
        self, value: SubscriptionInfoModel | SubscriptionManualInfoModel
    ) -> bool:
        query = None
        result = None
        if isinstance(value, SubscriptionInfoModel):
            query = select(SubscriptionInfoModel).where(
                SubscriptionInfoModel.id == value.id
            )

        elif isinstance(value, SubscriptionManualInfoModel):
            query = select(SubscriptionManualInfoModel).where(
                SubscriptionManualInfoModel.id == value.id
            )
        if query:
            result = session.execute(query).scalars().first()

        if query and result:
            return True
        return False

    def find_to_update(
        self,
        target_model: Type[SubscriptionInfoModel | SubscriptionManualInfoModel],
    ) -> list[SubscriptionInfoEntity | SubscriptionManualInfoEntity] | None:
        result_list = None

        if target_model == SubscriptionInfoModel:
            query = select(SubscriptionInfoModel).where(
                SubscriptionInfoModel.update_needed == True
            )
            results = session.execute(query).scalars().all()
            if results:
                result_list = [result.to_subs_info_entity() for result in results]

        elif target_model == SubscriptionManualInfoModel:
            query = select(SubscriptionManualInfoModel).where(
                SubscriptionManualInfoModel.update_needed == True
            )
            results = session.execute(query).scalars().all()
            if results:
                result_list = [
                    result.to_subs_manual_info_entity() for result in results
                ]

        return result_list

    def bulk_save_subscription_infos(self, create_list: list[dict]) -> None:
        failed_pk_list = list()
        try:
            session.bulk_insert_mappings(
                SubscriptionInfoModel, [create_info for create_info in create_list]
            )
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            logger.error(
                f"[SyncSubscriptionInfoRepository][bulk_save_subscription_infos] error : {e}"
            )
            for entry in create_list:
                failed_pk_list.append(entry["id"])
            logger.info(
                f"[SyncSubscriptionInfoRepository][bulk_save_subscription_infos]-failed_list: {len(failed_pk_list)}-{failed_pk_list})"
            )
            raise NotUniqueErrorException
