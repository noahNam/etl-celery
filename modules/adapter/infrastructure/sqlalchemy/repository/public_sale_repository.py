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

logger = logger_.getLogger(__name__)


class SyncPublicSaleRepository:
    def save_all(self, models: list[PublicSaleModel], sub_ids: list[int]) -> None:
        if not models:
            return None

        try:
            session.add_all(models)
            session.execute(
                update(SubscriptionModel)
                .where(SubscriptionModel.subs_id.in_(sub_ids))
                .values(update_needed=False)
            )
            session.commit()

        except Exception as e:
            logger.error(
                f"[SyncPublicSaleRepository][save_all][{type(models[0])}] updated_at : {models[0].updated_at} error : {e}"
            )
            session.rollback()
            raise Exception

    def find_to_detail_ids_by_sub_ids(
        self, sub_ids: list[int]
    ) -> list[PublicDtUniqueEntity]:
        query = select(PublicSaleDetailModel).where(
            PublicSaleDetailModel.public_sale_id.in_(sub_ids)
        )
        results = session.execute(query).scalars().all()
        return [result.to_unique_entity() for result in results]

    def save_all_details(
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
                    session.add(public_sales)
                else:
                    session.execute(
                        update(PublicSaleModel)
                        .where(PublicSaleModel.id == public_sale.id)
                        .values(
                            real_estate_id=public_sale.real_estate_id,
                            name=public_sale.name,
                            region=public_sale.region,
                            housing_category=public_sale.housing_category,
                            rent_type=public_sale.rent_type,
                            trade_type=public_sale.trade_type,
                            construct_company=public_sale.construct_company,
                            supply_household=public_sale.supply_household,
                            offer_date=public_sale.offer_date,
                            subscription_start_date=public_sale.subscription_start_date,
                            subscription_end_date=public_sale.subscription_end_date,
                            special_supply_date=public_sale.special_supply_date,
                            special_supply_etc_date=public_sale.special_supply_etc_date,
                            special_etc_gyeonggi_date=public_sale.special_etc_gyeonggi_date,
                            first_supply_date=public_sale.first_supply_date,
                            first_supply_etc_date=public_sale.first_supply_etc_date,
                            first_etc_gyeonggi_date=public_sale.first_etc_gyeonggi_date,
                            second_supply_date=public_sale.second_supply_date,
                            second_supply_etc_date=public_sale.second_supply_etc_date,
                            second_etc_gyeonggi_date=public_sale.second_etc_gyeonggi_date,
                            notice_winner_date=public_sale.notice_winner_date,
                            contract_start_date=public_sale.contract_start_date,
                            contract_end_date=public_sale.contract_end_date,
                            move_in_year=public_sale.move_in_year,
                            move_in_month=public_sale.move_in_month,
                            min_down_payment=public_sale.min_down_payment,
                            max_down_payment=public_sale.max_down_payment,
                            down_payment_ratio=public_sale.down_payment_ratio,
                            reference_url=public_sale.reference_url,
                            offer_notice_url=public_sale.offer_notice_url,
                            heating_type=public_sale.heating_type,
                            vl_rat=public_sale.vl_rat,
                            bc_rat=public_sale.bc_rat,
                            hhld_total_cnt=public_sale.hhld_total_cnt,
                            park_total_cnt=public_sale.park_total_cnt,
                            highest_floor=public_sale.highest_floor,
                            dong_cnt=public_sale.dong_cnt,
                            contact_amount=public_sale.contact_amount,
                            middle_amount=public_sale.middle_amount,
                            remain_amount=public_sale.remain_amount,
                            sale_limit=public_sale.sale_limit,
                            compulsory_residence=public_sale.compulsory_residence,
                            hallway_type=public_sale.hallway_type,
                            is_checked=public_sale.is_checked,
                            is_available=public_sale.is_available,
                            update_needed=True,
                        )
                    )
            for public_sale_detail in public_sale_details:
                exists_result: bool = self.exists_by_key(value=public_sale_detail)
                if exists_result:
                    session.add(public_sale_detail)
                else:
                    session.execute(
                        update(PublicSaleDetailModel)
                        .where(PublicSaleDetailModel.id == public_sale_detail.id)
                        .values(
                            area_type=public_sale_detail.area_type,
                            private_area=public_sale_detail.private_area,
                            supply_area=public_sale_detail.supply_area,
                            supply_price=public_sale_detail.supply_price,
                            acquisition_tax=public_sale_detail.acquisition_tax,
                            special_household=public_sale_detail.special_household,
                            multi_children_household=public_sale_detail.multi_children_household,
                            newlywed_household=public_sale_detail.newlywed_household,
                            old_parent_household=public_sale_detail.old_parent_household,
                            first_life_household=public_sale_detail.first_life_household,
                            general_household=public_sale_detail.general_household,
                            bay=public_sale_detail.bay,
                            pansang_tower=public_sale_detail.pansang_tower,
                            kitchen_window=public_sale_detail.kitchen_window,
                            direct_window=public_sale_detail.direct_window,
                            alpha_room=public_sale_detail.alpha_room,
                            cyber_model_house_link=public_sale_detail.cyber_model_house_link,
                            update_needed=True,
                        )
                    )

            for special_supply_result in special_supply_results:
                exists_result: bool = self.exists_by_key(value=special_supply_result)
                if exists_result:
                    session.add(special_supply_result)
                else:
                    session.execute(
                        update(SpecialSupplyResultModel)
                        .where(
                            and_(
                                SpecialSupplyResultModel.public_sale_detail_id
                                == special_supply_result.public_sale_detail_id,
                                SpecialSupplyResultModel.region
                                == special_supply_result.region,
                            )
                        )
                        .values(
                            public_sale_detail_id=special_supply_result.public_sale_detail_id,
                            region=special_supply_result.region,
                            region_percent=special_supply_result.region_percent,
                            multi_children_vol=special_supply_result.multi_children_vol,
                            newlywed_vol=special_supply_result.newlywed_vol,
                            old_parent_vol=special_supply_result.old_parent_vol,
                            first_life_vol=special_supply_result.first_life_vol,
                            update_needed=True,
                        )
                    )

            for general_supply_result in general_supply_results:
                exists_result: bool = self.exists_by_key(value=general_supply_result)
                if exists_result:
                    session.add(general_supply_result)
                else:
                    session.execute(
                        update(GeneralSupplyResultModel)
                        .where(
                            and_(
                                GeneralSupplyResultModel.public_sale_detail_id
                                == general_supply_result.public_sale_detail_id,
                                GeneralSupplyResultModel.region
                                == general_supply_result.region,
                            )
                        )
                        .values(
                            public_sale_detail_id=general_supply_result.public_sale_detail_id,
                            region=general_supply_result.region,
                            region_percent=general_supply_result.region_percent,
                            applicant_num=general_supply_result.applicant_num,
                            competition_rate=general_supply_result.competition_rate,
                            win_point=general_supply_result.win_point,
                            update_needed=True,
                        )
                    )

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
