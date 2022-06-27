from modules.adapter.infrastructure.etl import Transfer
from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptDealsJoinKeyEntity,
    GovtAptRentsJoinKeyEntity,
    GovtOfctlDealJoinKeyEntity,
    GovtOfctlRentJoinKeyEntity,
    GovtRightLotOutJoinKeyEntity
)
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    SupplyAreaEntity
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_deal_model import AptDealModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_rent_model import AptRentModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_deal_model import OfctlDealModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_rent_model import OfctlRentModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.right_lot_out_model import RightLotOutModel

from modules.adapter.infrastructure.utils.math_helper import MathHelper


class TransferAptDeals(Transfer):
    def start_transfer(self,
                       transfer_type: int,
                       entities: list[GovtAptDealsJoinKeyEntity
                                      | GovtOfctlDealJoinKeyEntity
                                      | GovtAptRentsJoinKeyEntity
                                      | GovtOfctlRentJoinKeyEntity
                                      | GovtRightLotOutJoinKeyEntity],
                       supply_areas: list[SupplyAreaEntity]
                       ) -> tuple[list[AptDealModel], list[int]] \
                            | tuple[list[AptRentModel], list[int]] \
                            | tuple[list[OfctlDealModel], list[int]] \
                            | tuple[list[OfctlRentModel], list[int]] \
                            | tuple[list[RightLotOutModel], list[int]] \
                            | None:

        if transfer_type == GovtFindTypeEnum.APT_DEALS_INPUT.value:
            apt_daels = list()
            apt_dael_ids = list()
            for govt_apt_deal in entities:
                supply_area = self._get_supply_area(supply_areas=supply_areas, govt_deal=govt_apt_deal)

                apt_dael = AptDealModel(
                    house_id=govt_apt_deal.house_id,
                    dong=govt_apt_deal.dong,
                    bld_name=govt_apt_deal.apt_name,
                    deal_amount=govt_apt_deal.deal_amount,
                    deal_year=govt_apt_deal.deal_year,
                    deal_month=govt_apt_deal.deal_month,
                    deal_day=govt_apt_deal.deal_day,
                    serial_no=govt_apt_deal.serial_no,
                    private_area=MathHelper().round(float(govt_apt_deal.exclusive_area), 2),
                    supply_area=supply_area,
                    regional_cd=govt_apt_deal.regional_cd,
                    floor=govt_apt_deal.floor,
                    cancel_deal_type=govt_apt_deal.cancel_deal_type,
                    cancel_deal_day=govt_apt_deal.cancel_deal_day,
                    req_gbn=govt_apt_deal.req_gbn,
                    rdealer_lawdnm=govt_apt_deal.rdealer_lawdnm,
                    is_available=True,
                )
                apt_daels.append(apt_dael)
                apt_dael_ids.append(govt_apt_deal.id)
            return apt_daels, apt_dael_ids

        elif transfer_type == GovtFindTypeEnum.APT_RENTS_INPUT.value:
            apt_rents = list()
            apt_rent_ids = list()
            for govt_apt_rent in entities:
                supply_area = self._get_supply_area(supply_areas=supply_areas, govt_deal=govt_apt_rent)

                apt_rent = AptRentModel(
                    house_id=govt_apt_rent.house_id,
                    dong=govt_apt_rent.house_id,
                    bld_name=govt_apt_rent.apt_name,
                    monthly_amount=govt_apt_rent.monthly_amount,
                    deal_year=govt_apt_rent.deal_year,
                    deal_month=govt_apt_rent.deal_month,
                    deal_day=govt_apt_rent.deal_day,
                    deposit=govt_apt_rent.deposit,
                    private_area=MathHelper().round(float(govt_apt_rent.exclusive_area), 2),
                    supply_area=supply_area,
                    regional_cd=govt_apt_rent.regional_cd,
                    floor=govt_apt_rent.floor,
                    is_available=True,
                )
                apt_rents.append(apt_rent)
                apt_rent_ids.append(govt_apt_rent.id)
            return apt_rents, apt_rent_ids

        elif transfer_type == GovtFindTypeEnum.OFCTL_DEAL_INPUT.value:
            ofctl_deals = list()
            ofctl_deal_ids = list()
            for govt_ofctl_deal in entities:
                supply_area = self._get_supply_area(supply_areas=supply_areas, govt_deal=govt_ofctl_deal)

                ofctl_deal = OfctlDealModel(
                    house_id=govt_ofctl_deal.house_id,
                    dong=govt_ofctl_deal.dong,
                    bld_name=govt_ofctl_deal.ofctl_name,
                    deal_amount=govt_ofctl_deal.deal_amount,
                    deal_month=govt_ofctl_deal.deal_month,
                    deal_day=govt_ofctl_deal.deal_day,
                    preivate_area=MathHelper().round(float(govt_ofctl_deal.exclusive_area), 2),
                    supply_area=supply_area,
                    regional_cd=govt_ofctl_deal.regional_cd,
                    floor=govt_ofctl_deal.floor,
                    cancel_deal_type=govt_ofctl_deal.cancel_deal_type,
                    cancel_deal_day=govt_ofctl_deal.cancel_deal_day,
                    req_gbn=govt_ofctl_deal.req_gbn,
                    rdealer_lawdnm=govt_ofctl_deal.rdealer_lawdnm,
                    is_available=True
                )
                ofctl_deals.append(ofctl_deal)
                ofctl_deal_ids.append(govt_ofctl_deal.id)
            return ofctl_deals, ofctl_deal_ids

        elif transfer_type == GovtFindTypeEnum.OFCTL_RENT_INPUT.value:
            ofctl_rents = list()
            ofctl_rent_ids = list()
            for govt_ofctl_rent in entities:
                supply_area = self._get_supply_area(supply_areas=supply_areas, govt_deal=govt_ofctl_rent)

                ofctl_rent = OfctlRentModel(
                    house_id=govt_ofctl_rent.house_id,
                    dong=govt_ofctl_rent.dong,
                    bld_name=govt_ofctl_rent.ofctl_name,
                    deal_year=govt_ofctl_rent.deal_year,
                    deal_month=govt_ofctl_rent.deal_month,
                    deal_day=govt_ofctl_rent.deal_day,
                    deposit=govt_ofctl_rent.deposit,
                    monthly_amount=govt_ofctl_rent.monthly_amount,
                    private_area=MathHelper().round(float(govt_ofctl_rent.exclusive_area), 2),
                    supply_atra=supply_area,
                    regional_cd=govt_ofctl_rent.regional_cd,
                    floor=govt_ofctl_rent.floor,
                    is_available=True,
                )
                ofctl_rents.append(ofctl_rent)
                ofctl_rent_ids.append(govt_ofctl_rent.id)
            return ofctl_rents, ofctl_rent_ids

        elif transfer_type == GovtFindTypeEnum.RIGHT_LOT_OUT_INPUT.value:
            right_lot_outs = list()
            right_lot_out_ids = list()

            for govt_right_lot_out in entities:
                supply_area = self._get_supply_area(supply_areas=supply_areas, govt_deal=govt_right_lot_out)

                right_lot_out = RightLotOutModel(
                    house_id=govt_right_lot_out.house_id,
                    dong=govt_right_lot_out.dong,
                    bld_name=govt_right_lot_out.name,
                    deal_amount=govt_right_lot_out.deal_amount,
                    classification_owner_ship=govt_right_lot_out.classification_owner_ship,
                    deal_year=govt_right_lot_out.deal_year,
                    deal_month=govt_right_lot_out.deal_month,
                    deal_day=govt_right_lot_out.deal_day,
                    private_area=MathHelper().round(float(govt_right_lot_out.exclusive_area), 2),
                    supply_area=supply_area,
                    regional_cd=govt_right_lot_out.regional_cd,
                    floor=govt_right_lot_out.floor,
                    is_available=True,
                )
                right_lot_outs.append(right_lot_out)
                right_lot_out_ids.append(govt_right_lot_out.id)
            return right_lot_outs, right_lot_out_ids

        else:
            return None

    def _get_supply_area(self,
                         supply_areas: list[SupplyAreaEntity],
                         govt_deal: GovtAptDealsJoinKeyEntity
                                      | GovtOfctlDealJoinKeyEntity
                                      | GovtAptRentsJoinKeyEntity
                                      | GovtOfctlRentJoinKeyEntity
                                      | GovtRightLotOutJoinKeyEntity
                         ) -> float | None:
        if not supply_areas:
            return None

        supply_area = None
        for supply_entity in supply_areas:
            if govt_deal.house_id == supply_entity.house_id \
                    and govt_deal.exclusive_area == supply_entity.private_area:
                supply_area = supply_entity.supply_area
        return supply_area
