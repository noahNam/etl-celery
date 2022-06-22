from typing import Type

from sqlalchemy import exc, select, update

from core.domain.warehouse.subscription.interface.subscription_info_repository import (
    SubscriptionRepository,
)
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_detail_model import (
    SubscriptionDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_model import (
    SubscriptionModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.subscription_entity import (
    SubsToPublicEntity
)

logger = logger_.getLogger(__name__)


class SyncSubscriptionRepository(SubscriptionRepository):
    def save(self, value: SubscriptionModel | SubscriptionDetailModel) -> None:
        try:
            session.add(value)
            session.commit()
        except exc.IntegrityError as e:
            logger.error(
                f"[SyncSubscriptionRepository][save] target_model : {value} error : {e}"
            )
            session.rollback()
            raise NotUniqueErrorException

    def update(self, value: SubscriptionModel | SubscriptionDetailModel) -> None:
        if isinstance(value, SubscriptionModel):
            session.execute(
                update(SubscriptionModel)
                .where(SubscriptionModel.subs_id == value.subs_id)
                .values(
                    offer_date=value.offer_date,
                    notice_winner_date=value.notice_winner_date,
                    name=value.name,
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
                    region=value.region,
                    housing_category=value.housing_category,
                    rent_type=value.rent_type,
                    construct_company=value.construct_company,
                    contact=value.contact,
                    subscription_date=value.subscription_date,
                    special_supply_status=value.special_supply_status,
                    cmptt_rank=value.cmptt_rank,
                )
            )

        elif isinstance(value, SubscriptionDetailModel):
            session.execute(
                update(SubscriptionDetailModel)
                .where(SubscriptionDetailModel.id == value.id)
                .values(
                    subs_id=value.subs_id,
                    area_type=value.area_type,
                    supply_price=value.supply_price,
                    supply_area=value.supply_area,
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
                )
            )

        session.commit()

    def exists_by_key(self, value: SubscriptionModel | SubscriptionDetailModel) -> bool:
        query = None
        if isinstance(value, SubscriptionModel):
            query = select(SubscriptionModel).where(
                SubscriptionModel.subs_id == value.subs_id
            )

        elif isinstance(value, SubscriptionDetailModel):
            query = select(SubscriptionDetailModel).where(
                SubscriptionDetailModel.id == value.id
            )

        result = session.execute(query).scalars().first()

        if result:
            return True

        return False

    def dynamic_update(
        self,
        target_model: Type[SubscriptionModel | SubscriptionDetailModel],
        value: dict,
    ) -> None:
        if target_model == SubscriptionModel:
            key = value.get("key")
            items = value.get("items")
            query = select(SubscriptionModel).where(SubscriptionModel.subs_id == key)
            col_info = session.execute(query).scalars().first()

            if col_info:
                for (key, value) in items.items():
                    if hasattr(target_model, key):
                        setattr(col_info, key, value)
                        session.commit()

        elif target_model == SubscriptionDetailModel:
            key = value.get("key")
            items = value.get("items")
            query = select(target_model).where(SubscriptionDetailModel.id == key)
            col_info = session.execute(query).scalars().first()

            if col_info:
                for (key, value) in items.items():
                    if hasattr(target_model, key):
                        setattr(col_info, key, value)
                        session.commit()

    def find_by_update_needed(self) -> list[SubsToPublicEntity] | None:
        query = select(SubscriptionModel).where(
            SubscriptionModel.update_needed == True,
        )
        results = session.execute(query).scalars().all()
        if results:
            return [result.to_type_info_entity() for result in results]
        else:
            return None
