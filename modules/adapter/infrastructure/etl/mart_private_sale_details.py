from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.bld_deal_entity import (
    AptDealEntity,
    AptRentEntity,
    OfctlDealEntity,
    OfctlRentEntity,
    RightLotOutEntity,
)
from modules.adapter.infrastructure.sqlalchemy.enum.private_sale_enum import (
    PrivateSaleTradeTypeEnum,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_detail_model import (
    PrivateSaleDetailModel,
)


class TransformPrivateSaleDetail:
    def start_etl(
        self,
        target_list: list[
            AptDealEntity
            | AptRentEntity
            | OfctlDealEntity
            | OfctlRentEntity
            | RightLotOutEntity
        ],
    ) -> list[PrivateSaleDetailModel] | None:
        if not target_list:
            return None

        return self._etl_private_sale_details(target_list=target_list)

    def _etl_private_sale_details(
        self,
        target_list: list[
            AptDealEntity
            | AptRentEntity
            | OfctlDealEntity
            | OfctlRentEntity
            | RightLotOutEntity
        ],
    ) -> list[PrivateSaleDetailModel]:
        results = list()

        # todo. 1. 전월세 -> 전세/월세 구분 (PrivateSaleTradeTypeEnum) /  2. classification_owner_ship -> 분양입주권 구분
        if isinstance(target_list[0], AptDealEntity):
            for target_obj in target_list:
                contract_date = self._get_contract_date(target_obj=target_obj)
                results.append(
                    PrivateSaleDetailModel(
                        id=target_obj.id,
                        private_sale_id=target_obj.house_id,
                        private_area=target_obj.private_area,
                        supply_area=target_obj.supply_area,
                        contract_date=contract_date,
                        contract_ym=int(contract_date[-2:]),
                        trade_price=target_obj.deal_amount,
                        floor=int(target_obj.floor),
                        trade_type=PrivateSaleTradeTypeEnum.TRADING.value,
                        is_available=target_obj.is_available,
                        update_needed=target_obj.update_needed,
                    )
                )

        elif isinstance(target_list[0], AptRentEntity):
            for target_obj in target_list:
                contract_date = self._get_contract_date(target_obj=target_obj)
                results.append(
                    PrivateSaleDetailModel(
                        id=target_obj.id,
                        private_sale_id=target_obj.house_id,
                        private_area=target_obj.private_area,
                        supply_area=target_obj.supply_area,
                        contract_date=contract_date,
                        contract_ym=int(contract_date[-2:]),
                        deposit_price=target_obj.deposit,
                        rent_price=target_obj.monthly_amount,
                        floor=int(target_obj.floor),
                        trade_type=PrivateSaleTradeTypeEnum.MONTHLY_RENT.value,
                        is_available=target_obj.is_available,
                        update_needed=target_obj.update_needed,
                    )
                )

        elif isinstance(target_list[0], OfctlDealEntity):
            for target_obj in target_list:
                contract_date = self._get_contract_date(target_obj=target_obj)
                results.append(
                    PrivateSaleDetailModel(
                        id=target_obj.id,
                        private_sale_id=target_obj.house_id,
                        private_area=target_obj.private_area,
                        supply_area=target_obj.supply_area,
                        contract_date=contract_date,
                        contract_ym=int(contract_date[-2:]),
                        trade_price=target_obj.deal_amount,
                        floor=int(target_obj.floor),
                        trade_type=PrivateSaleTradeTypeEnum.TRADING.value,
                        is_available=target_obj.is_available,
                        update_needed=target_obj.update_needed,
                    )
                )

        elif isinstance(target_list[0], OfctlRentEntity):
            for target_obj in target_list:
                contract_date = self._get_contract_date(target_obj=target_obj)
                results.append(
                    PrivateSaleDetailModel(
                        id=target_obj.id,
                        private_sale_id=target_obj.house_id,
                        private_area=target_obj.private_area,
                        supply_area=target_obj.supply_area,
                        contract_date=contract_date,
                        contract_ym=int(contract_date[-2:]),
                        deposit_price=target_obj.deposit,
                        rent_price=target_obj.monthly_amount,
                        floor=int(target_obj.floor),
                        trade_type=PrivateSaleTradeTypeEnum.MONTHLY_RENT.value,
                        is_available=target_obj.is_available,
                        update_needed=target_obj.update_needed,
                    )
                )

        elif isinstance(target_list[0], RightLotOutEntity):
            for target_obj in target_list:
                contract_date = self._get_contract_date(target_obj=target_obj)
                results.append(
                    PrivateSaleDetailModel(
                        id=target_obj.id,
                        private_sale_id=target_obj.house_id,
                        private_area=target_obj.private_area,
                        supply_area=target_obj.supply_area,
                        contract_date=contract_date,
                        contract_ym=int(contract_date[-2:]),
                        trade_price=target_obj.deal_amount,
                        floor=int(target_obj.floor),
                        trade_type=PrivateSaleTradeTypeEnum.PUBLIC_TRADE.value,
                        is_available=target_obj.is_available,
                        update_needed=target_obj.update_needed,
                    )
                )

        return results

    def _get_contract_date(
        self,
        target_obj: AptDealEntity
        | AptRentEntity
        | OfctlDealEntity
        | OfctlRentEntity
        | RightLotOutEntity,
    ) -> str:
        return target_obj.deal_day + target_obj.deal_month + target_obj.deal_day
