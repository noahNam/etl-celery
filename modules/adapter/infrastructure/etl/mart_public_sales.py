from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.subscription_entity import (
    SubsToPublicEntity
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_model import (
    PublicSaleModel
)

class TransformPublicSales:
    def start_transfer(self, subscriptions: list[SubsToPublicEntity]) -> list[PublicSaleModel]:
        return_models = list()
        for subscription in subscriptions:
            subscription_start_date: str = self._get_start_date(date=subscription.subscription_date)
            subscription_end_date: str = self._get_end_date(date=subscription.subscription_date)
            contract_start_date: str = self._get_start_date(date=subscription.contract_date)
            contract_end_date: str = self._get_end_date(date=subscription.contract_date)
            move_in_year, move_in_month = self._get_move_year_month(move_in_year=subscription.move_in_date)

            public_sale = PublicSaleModel(
                real_estate_id=None,  # todo, place_id 아직 없음
                name=subscription.name,
                region=subscription.region,
                housing_category=subscription.housing_category,
                rent_type=subscription.rent_type,
                trade_type=None,  # todo, 아직 데이터 없음
                construct_company=subscription.construct_company,
                supply_household=subscription.supply_household,
                offer_date=subscription.offer_date,
                subscription_start_date=subscription_start_date,
                subscription_end_date=subscription_end_date,
                special_supply_date=subscription.special_supply_date,
                special_supply_etc_date=subscription.special_supply_etc_date,
                special_etc_gyeonggi_date=subscription.special_etc_gyeonggi_date,
                first_supply_date=subscription.first_supply_date,
                first_supply_etc_date=subscription.first_supply_etc_date,
                first_etc_gyeonggi_date=subscription.first_etc_gyeonggi_date,
                second_supply_date=subscription.second_supply_date,
                second_supply_etc_date=subscription.second_supply_etc_date,
                second_etc_gyeonggi_date=subscription.second_etc_gyeonggi_date,
                notice_winner_date=subscription.notice_winner_date,
                contract_start_date=contract_start_date,
                contract_end_date=contract_end_date,
                move_in_year=move_in_year,
                move_in_month=move_in_month,
                min_down_payment=subscription.min_down_payment,
                max_down_payment=subscription.max_down_payment,
                down_payment_ratio=subscription.deposit,
                reference_url=subscription.cyber_model_house_link,
                offer_notice_url=subscription.offer_notice_url,
                heating_type=subscription.heat_type,
                vl_rat=subscription.vl_rat,
                bc_rat=subscription.bc_rat,
                hhld_total_cnt=subscription.hhld_total_cnt,
                park_total_cnt=subscription.park_total_cnt,
                highest_floor=subscription.highest_floor,
                dong_cnt=subscription.dong_cnt,
                contact_amount=subscription.deposit,
                middle_amount=subscription.middle_payment,
                remain_amount=subscription.balance,
                sale_limit=subscription.restriction_sale,
                compulsory_residence=subscription.compulsory_residence,
                hallway_type=subscription.hallway_type,
                is_checked=False,
                is_available=False,
                update_needed=True
            )
            return_models.append(public_sale)
        return return_models

    def _get_start_date(self, date: str) -> str | None:
        if date and len(date) == 23:
            return date[:10]
        else:
            return

    def _get_end_date(self, date: str) -> str | None:
        if date and len(date) == 23:
            return date[13:]
        else:
            return

    def _get_move_year_month(self, move_in_year: str) -> list[str] | None:
        if move_in_year and len(move_in_year) == 7:
            return [move_in_year[:4], move_in_year[5:7]]
        else:
            return None



