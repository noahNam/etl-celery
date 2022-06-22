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
            subscription_start_date = self._get_start_date(date=subscription.subscription_date)
            subscription_end_date = self._get_end_date(date=subscription.subscription_date)
            contract_start_date = self._get_start_date(date=subscription.contract_date)
            contract_end_date = self._get_end_date(date=subscription.contract_date)

            public_sale = PublicSaleModel(
                real_estate_id=None,
                name=subscription.name,
                region=subscription.region,
                housing_category=subscription.housing_category,
                rent_type=subscription.rent_type,
                trade_type=None,
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
                move_in_year=subscription.move_in_year,

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

    def get_move_year_month(self, move_in_year) -> list[str]:
        if move_in_year and len(move_in_year) == 7:
            return [move_in_year[13:], ]
        else:
            return



