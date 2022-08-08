from sqlalchemy import select, update, and_

from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.entity.datamart.v1.public_sale_entity import (
    PublicDtUniqueEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.general_supply_result_model import (
    GeneralSupplyResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_detail_model import (
    PublicSaleDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_model import (
    PublicSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.special_supply_result_model import (
    SpecialSupplyResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_detail_model import (
    SubscriptionDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_model import (
    SubscriptionModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.adapter.infrastructure.message.broker.redis import RedisClient

logger = logger_.getLogger(__name__)


class SyncPublicSaleRepository:
    def save_public_sales(
        self,
        public_sales: list[PublicSaleModel],
        sub_ids: list[int],
        public_sale_details: list[PublicSaleDetailModel],
        special_supply_results: list[SpecialSupplyResultModel],
        general_supply_results: list[GeneralSupplyResultModel],
        sub_detail_ids: list[int],
    ) -> None:
        if not public_sales:
            return None

        try:
            for public_sale in public_sales:
                exists_result: bool = self.exists_by_key(value=public_sale)
                if exists_result:
                    self.update(public_sale)
                else:
                    self.save(public_sale)

            for public_sale_detail in public_sale_details:
                exists_result: bool = self.exists_by_key(value=public_sale_detail)
                if exists_result:
                    self.update(public_sale_detail)
                else:
                    self.save(public_sale_detail)

            for special_supply_result in special_supply_results:
                exists_result: bool = self.exists_by_key(value=special_supply_result)
                if exists_result:
                    self.update(special_supply_result)
                else:
                    self.save(special_supply_result)

            for general_supply_result in general_supply_results:
                exists_result: bool = self.exists_by_key(value=general_supply_result)
                if exists_result:
                    self.update(general_supply_result)
                else:
                    self.save(general_supply_result)

            session.execute(
                update(SubscriptionModel)
                .where(SubscriptionModel.subs_id.in_(sub_ids))
                .values(update_needed=False)
            )

            session.execute(
                update(SubscriptionDetailModel)
                .where(SubscriptionDetailModel.id.in_(sub_detail_ids))
                .values(update_needed=False)
            )
            session.commit()

        except Exception as e:
            logger.error(
                f"[SyncPublicSaleRepository][save_all_update_needed][error : {e}]"
            )
            session.rollback()
            raise Exception

    def save(
        self,
        model: PublicSaleModel
        | PublicSaleDetailModel
        | SpecialSupplyResultModel
        | GeneralSupplyResultModel,
    ) -> None:
        session.add(model)

    def update(
        self,
        model: PublicSaleModel
        | PublicSaleDetailModel
        | SpecialSupplyResultModel
        | GeneralSupplyResultModel,
    ) -> None:
        if isinstance(model, PublicSaleModel):
            session.execute(
                update(PublicSaleModel)
                .where(PublicSaleModel.id == model.id)
                .values(
                    real_estate_id=model.real_estate_id,
                    name=model.name,
                    region=model.region,
                    housing_category=model.housing_category,
                    rent_type=model.rent_type,
                    trade_type=model.trade_type,
                    construct_company=model.construct_company,
                    supply_household=model.supply_household,
                    offer_date=model.offer_date,
                    subscription_start_date=model.subscription_start_date,
                    subscription_end_date=model.subscription_end_date,
                    special_supply_date=model.special_supply_date,
                    special_supply_etc_date=model.special_supply_etc_date,
                    special_etc_gyeonggi_date=model.special_etc_gyeonggi_date,
                    first_supply_date=model.first_supply_date,
                    first_supply_etc_date=model.first_supply_etc_date,
                    first_etc_gyeonggi_date=model.first_etc_gyeonggi_date,
                    second_supply_date=model.second_supply_date,
                    second_supply_etc_date=model.second_supply_etc_date,
                    second_etc_gyeonggi_date=model.second_etc_gyeonggi_date,
                    notice_winner_date=model.notice_winner_date,
                    contract_start_date=model.contract_start_date,
                    contract_end_date=model.contract_end_date,
                    move_in_year=model.move_in_year,
                    move_in_month=model.move_in_month,
                    min_down_payment=model.min_down_payment,
                    max_down_payment=model.max_down_payment,
                    down_payment_ratio=model.down_payment_ratio,
                    reference_url=model.reference_url,
                    offer_notice_url=model.offer_notice_url,
                    heating_type=model.heating_type,
                    vl_rat=model.vl_rat,
                    bc_rat=model.bc_rat,
                    hhld_total_cnt=model.hhld_total_cnt,
                    park_total_cnt=model.park_total_cnt,
                    highest_floor=model.highest_floor,
                    dong_cnt=model.dong_cnt,
                    contact_amount=model.contact_amount,
                    middle_amount=model.middle_amount,
                    remain_amount=model.remain_amount,
                    sale_limit=model.sale_limit,
                    compulsory_residence=model.compulsory_residence,
                    hallway_type=model.hallway_type,
                    is_checked=model.is_checked,
                    is_available=model.is_available,
                    update_needed=True,
                )
            )
        elif isinstance(model, PublicSaleDetailModel):
            session.execute(
                update(PublicSaleDetailModel)
                .where(PublicSaleDetailModel.id == model.id)
                .values(
                    area_type=model.area_type,
                    private_area=model.private_area,
                    supply_area=model.supply_area,
                    supply_price=model.supply_price,
                    acquisition_tax=model.acquisition_tax,
                    special_household=model.special_household,
                    multi_children_household=model.multi_children_household,
                    newlywed_household=model.newlywed_household,
                    old_parent_household=model.old_parent_household,
                    first_life_household=model.first_life_household,
                    general_household=model.general_household,
                    bay=model.bay,
                    pansang_tower=model.pansang_tower,
                    kitchen_window=model.kitchen_window,
                    direct_window=model.direct_window,
                    alpha_room=model.alpha_room,
                    cyber_model_house_link=model.cyber_model_house_link,
                    update_needed=True,
                )
            )
        elif isinstance(model, SpecialSupplyResultModel):
            session.execute(
                update(SpecialSupplyResultModel)
                .where(
                    and_(
                        SpecialSupplyResultModel.public_sale_detail_id
                        == model.public_sale_detail_id,
                        SpecialSupplyResultModel.region == model.region,
                    )
                )
                .values(
                    public_sale_detail_id=model.public_sale_detail_id,
                    region=model.region,
                    region_percent=model.region_percent,
                    multi_children_vol=model.multi_children_vol,
                    newlywed_vol=model.newlywed_vol,
                    old_parent_vol=model.old_parent_vol,
                    first_life_vol=model.first_life_vol,
                    update_needed=True,
                )
            )
        elif isinstance(model, GeneralSupplyResultModel):
            session.execute(
                update(GeneralSupplyResultModel)
                .where(
                    and_(
                        GeneralSupplyResultModel.public_sale_detail_id
                        == model.public_sale_detail_id,
                        GeneralSupplyResultModel.region == model.region,
                    )
                )
                .values(
                    public_sale_detail_id=model.public_sale_detail_id,
                    region=model.region,
                    region_percent=model.region_percent,
                    applicant_num=model.applicant_num,
                    competition_rate=model.competition_rate,
                    win_point=model.win_point,
                    update_needed=True,
                )
            )
        else:
            return None

    def exists_by_key(
        self,
        value: [
            PublicSaleModel
            | PublicSaleDetailModel
            | SpecialSupplyResultModel
            | GeneralSupplyResultModel
        ],
    ) -> bool:
        result = None
        if isinstance(value, PublicSaleModel):
            query = select(PublicSaleModel.id).where(PublicSaleModel.id == value.id)
            result = session.execute(query).scalars().first()
        elif isinstance(value, PublicSaleDetailModel):
            query = select(PublicSaleDetailModel.id).where(
                PublicSaleDetailModel.id == value.id
            )
            result = session.execute(query).scalars().first()
        elif isinstance(value, SpecialSupplyResultModel):
            query = select(
                SpecialSupplyResultModel.public_sale_detail_id,
                SpecialSupplyResultModel.region,
            ).where(
                and_(
                    SpecialSupplyResultModel.public_sale_detail_id
                    == value.public_sale_detail_id,
                    SpecialSupplyResultModel.region == value.region,
                )
            )
            result = session.execute(query).scalars().first()

        elif isinstance(value, GeneralSupplyResultModel):
            query = select(
                GeneralSupplyResultModel.public_sale_detail_id,
                GeneralSupplyResultModel.region,
            ).where(
                and_(
                    GeneralSupplyResultModel.public_sale_detail_id
                    == value.public_sale_detail_id,
                    GeneralSupplyResultModel.region == value.region,
                )
            )
            result = session.execute(query).scalars().first()

        if result:
            return True
        else:
            return False

    def find_by_updated_needed(
        self,
        target_model: type[SpecialSupplyResultModel | GeneralSupplyResultModel]
    ) -> list[SpecialSupplyResultModel] | list[GeneralSupplyResultModel]:
        try:
            query = select(target_model).where(
                target_model.update_needed == True,
            )
            result = session.execute(query).scalars().all()
            return result

        except Exception as e:
            logger.error(
                f"[SyncPublicSaleRepository][save_all_update_needed][error : {e}]"
            )
            session.rollback()
            raise Exception

    def update_by_update_needed(
            self
    ) -> None:
        try:
            models = [
                PublicSaleModel,
                PublicSaleDetailModel,
                SpecialSupplyResultModel,
                GeneralSupplyResultModel,
            ]
            for model in models:
                session.execute(
                    update(
                        model
                    ).where(
                        model.update_needed == True,
                    ).values(
                        update_needed=False
                    )
                )
            session.commit()

        except Exception as e:
            logger.error(
                f"[SyncPublicSaleRepository][save_all_update_needed][error : {e}]"
            )
            session.rollback()
            raise Exception