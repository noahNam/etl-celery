from modules.adapter.infrastructure.etl import Transfer
from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptDealsJoinKeyEntity,
    GovtAptRentsJoinKeyEntity,
    GovtOfctlDealJoinKeyEntity,
    GovtOfctlRentJoinKeyEntity,
    GovtRightLotOutJoinKeyEntity
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
                                      | GovtRightLotOutJoinKeyEntity]
                       ) -> list[AptDealModel]\
                            | list[AptRentModel]\
                            | list[OfctlDealModel]\
                            | list[OfctlRentModel]\
                            | list[RightLotOutModel]\
                            | None:

        if transfer_type == GovtFindTypeEnum.APT_DEALS_INPUT.value:
            apt_daels = list()
            for govt_apt_deal in entities:
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
                    supply_area=None,  # fixme: 채워넣기
                    regional_cd=govt_apt_deal.regional_cd,
                    floor=govt_apt_deal.floor,
                    cancel_deal_type=govt_apt_deal.cancel_deal_type,
                    cancel_deal_day=govt_apt_deal.cancel_deal_day,
                    req_gbn=govt_apt_deal.req_gbn,
                    rdealer_lawdnm=govt_apt_deal.rdealer_lawdnm,
                    is_available=True,
                )
                apt_daels.append(apt_dael)
            return apt_daels

        elif transfer_type == GovtFindTypeEnum.APT_RENTS_INPUT.value:
            apt_rents = list()
            for govt_apt_rent in entities:
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
                    supply_area=None,
                    regional_cd=govt_apt_rent.regional_cd,
                    floor=govt_apt_rent.floor,
                    is_available=True,
                )
                apt_rents.append(apt_rent)
            return apt_rents

        elif transfer_type == GovtFindTypeEnum.OFCTL_DEAL_INPUT.value:
            ofctl_deals = list()
            for govt_ofctl_deal in entities:
                ofctl_deal = OfctlDealModel(
                    house_id=govt_ofctl_deal.house_id,
                    dong=govt_ofctl_deal.dong,
                    bld_name=govt_ofctl_deal.ofctl_name,
                    deal_amount=govt_ofctl_deal.deal_amount,
                    deal_month=govt_ofctl_deal.deal_month,
                    deal_day=govt_ofctl_deal.deal_day,
                    preivate_area=MathHelper().round(float(govt_ofctl_deal.exclusive_area), 2),
                    supply_area=None,
                    regional_cd=govt_ofctl_deal.regional_cd,
                    floor=govt_ofctl_deal.floor,
                    cancel_deal_type=govt_ofctl_deal.cancel_deal_type,
                    cancel_deal_day=govt_ofctl_deal.cancel_deal_day,
                    req_gbn=govt_ofctl_deal.req_gbn,
                    rdealer_lawdnm=govt_ofctl_deal.rdealer_lawdnm,
                    is_available=True
                )
                ofctl_deals.append(ofctl_deal)
            return ofctl_deals

        elif transfer_type == GovtFindTypeEnum.OFCTL_RENT_INPUT.value:
            ofctl_rents = list()
            for govt_ofctl_rent in entities:
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
                    supply_atra=None,
                    regional_cd=govt_ofctl_rent.regional_cd,
                    floor=govt_ofctl_rent.floor,
                    is_available=True,
                )
                ofctl_rents.append(ofctl_rent)
            return ofctl_rents

        elif transfer_type == GovtFindTypeEnum.RIGHT_LOT_OUT_INPUT.value:
            right_lot_outs = list()
            for govt_right_lot_out in entities:
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
                    supply_area=None,
                    regional_cd=govt_right_lot_out.regional_cd,
                    floor=govt_right_lot_out.floor,
                    is_available=True,
                )
                right_lot_outs.append(right_lot_out)
            return right_lot_outs

        else:
            return None



