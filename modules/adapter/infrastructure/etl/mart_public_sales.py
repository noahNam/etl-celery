import re

from modules.adapter.infrastructure.utils.math_helper import MathHelper
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.subscription_entity import (
    SubsToPublicEntity,
    SubDtToPublicDtEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_model import (
    PublicSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_detail_model import (
    PublicSaleDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.special_supply_result_model import (
    SpecialSupplyResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datamart.v1.public_sale_entity import (
    PublicDtUniqueEntity,
)


class TransformPublicSales:
    def start_transfer_public_sales(
        self, subscriptions: list[SubsToPublicEntity]
    ) -> list[PublicSaleModel]:
        return_models = list()
        for subscription in subscriptions:
            subscription_start_date: str = self._get_start_date(
                date=subscription.subscription_date
            )
            subscription_end_date: str = self._get_end_date(
                date=subscription.subscription_date
            )
            contract_start_date: str = self._get_start_date(
                date=subscription.contract_date
            )
            contract_end_date: str = self._get_end_date(date=subscription.contract_date)
            move_in_year, move_in_month = self._get_move_year_month(
                move_in_year=subscription.move_in_date
            )

            public_sale = PublicSaleModel(
                real_estate_id=subscription.place_id,
                name=subscription.name,
                region=subscription.region,
                housing_category=subscription.housing_category,
                rent_type=subscription.rent_type,
                trade_type=None,  # todo, 아직 데이터 없음
                construct_company=subscription.construct_company,
                supply_household=float(subscription.supply_household),
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
                reference_url=subscription.hompage_url,
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
                update_needed=True,
            )
            return_models.append(public_sale)
        return return_models

    def start_transfer_public_sale_details(
        self, sub_details: list[SubDtToPublicDtEntity]
    ) -> list[PublicSaleDetailModel]:
        return_models = list()
        for sub_detail in sub_details:
            area_type: str = self._get_area_type(raw_type=sub_detail.area_type)
            private_area: float = self._get_private_area(raw_type=sub_detail.area_type)
            acquisition_tax: int = self._calculate_house_acquisition_xax(
                private_area=private_area, supply_price=int(sub_detail.supply_price)
            )

            public_sale_detail = PublicSaleDetailModel(
                public_sale_id=sub_detail.subs_id,
                area_type=area_type,
                private_area=private_area,
                supply_area=MathHelper.round(float(sub_detail.supply_area), 2),
                supply_price=int(sub_detail.supply_price),
                acquisition_tax=acquisition_tax,
                special_household=float(sub_detail.special_household),
                multi_children_household=float(sub_detail.multi_children_household),
                newlywed_household=float(sub_detail.newlywed_household),
                old_parent_household=float(sub_detail.old_parent_household),
                first_life_household=float(sub_detail.first_life_household),
                general_household=float(sub_detail.general_household),
                bay=sub_detail.bay,
                pansang_tower=sub_detail.pansang_tower,
                kitchen_window=sub_detail.kitchen_window,
                direct_window=sub_detail.direct_window,
                alpha_room=sub_detail.alpha_room,
                cyber_model_house_link=sub_detail.cyber_model_house_link,
                update_needed=True,
            )
            return_models.append(public_sale_detail)

        return return_models

    def start_transfer_special_supply_results(
        self,
        sub_details: list[SubDtToPublicDtEntity],
        public_sale_detail_ids: list[PublicDtUniqueEntity],
    ) -> list[SpecialSupplyResultModel]:
        return_models = list()
        for sub_detail in sub_details:
            public_sale_detail_id: int = self._get_public_sale_detail_id(
                sub_detail=sub_detail, public_sale_details=public_sale_detail_ids
            )
            if not public_sale_detail_id:
                continue

            # region_percents: [해당지역, 기타경기, 기타지역]
            region_percents: list[int] = self._get_region_percent(sub_detail=sub_detail)

            area = SpecialSupplyResultModel(
                public_sale_detail_id=public_sale_detail_id,
                region="해당지역",
                region_percent=region_percents[0],
                multi_children_vol=sub_detail.multi_children_vol,
                newlywed_vol=sub_detail.newlywed_vol,
                old_parent_vol=sub_detail.old_parent_vol,
                first_life_vol=sub_detail.first_life_vol,
                update_needed=False,
            )
            gyeonggi_area = SpecialSupplyResultModel(
                public_sale_detail_id=public_sale_detail_id,
                region="기타경기",
                region_percent=region_percents[1],
                multi_children_vol=sub_detail.multi_children_vol_etc_gyeonggi,
                newlywed_vol=sub_detail.newlywed_vol_etc_gyeonggi,
                old_parent_vol=sub_detail.old_parent_vol_etc_gyeonggi,
                first_life_vol=sub_detail.first_life_vol_etc_gyeonggi,
                update_needed=False,
            )
            etc_area = SpecialSupplyResultModel(
                public_sale_detail_id=public_sale_detail_id,
                region="기타지역",
                region_percent=region_percents[2],
                multi_children_vol=sub_detail.multi_children_vol_etc,
                newlywed_vol=sub_detail.newlywed_vol_etc,
                old_parent_vol=sub_detail.old_parent_vol_etc,
                first_life_vol=sub_detail.first_life_vol_etc,
                update_needed=False,
            )

            return_models.append(area)
            return_models.append(gyeonggi_area)
            return_models.append(etc_area)
        return return_models

    def _get_start_date(self, date: str) -> str | None:
        if date and len(date) == 23:
            return date[:10]
        else:
            return None

    def _get_end_date(self, date: str) -> str | None:
        if date and len(date) == 23:
            return date[13:]
        else:
            return None

    def _get_move_year_month(self, move_in_year: str) -> list[str] | None:
        if move_in_year and len(move_in_year) == 7:
            return [move_in_year[:4], move_in_year[5:7]]
        else:
            return None

    def _get_area_type(self, raw_type: str) -> str | None:
        val = re.search("([a-zA-Z]+)", raw_type)
        return val[0] if val else None

    def _get_private_area(self, raw_type: str) -> float:
        val = re.search("([0-9]+[.][0-9]+)", raw_type)
        return MathHelper().round(float(val[0]), 2)

    def _calculate_house_acquisition_xax(
        self, private_area: float, supply_price: int
    ) -> int:
        """
        부동산 정책이 매년 변경되므로 정기적으로 세율 변경 시 업데이트 필요합니다.
        <취득세 계산 2022년도 기준>
        - 전용면적을 사용 (공급면적 X)
        - 부동산 종류가 주택일 경우로 한정 (상가, 오피스텔, 토지, 건물 제외)
        - 1주택자 기준

        [parameters]
        - private_area: 전용면적(제곱미터)
        - supply_price: 공급금액 (DB 저장 단위: 만원)

        [계산법]
        6억 이하, 85제곱미터 이하 : 1.1%
        6억 이하, 85제곱미터 초과 : 1.3%
        6억 초과 9억 이하, 85제곱미터 이하 : (집값 x 2 / 3억 - 3) * 0.01 * 1.1
        6억 초과 9억 이하, 85제곱미터 초과 : (집값 x 2 / 3억 - 3) * 0.01 * 1.1 + 0.002
        9억 초과, 85제곱미터 이하 : 3.3%
        9억 초과, 85제곱미터 초과 : 3.5%

        [return]
        - total_acquisition_tax : 최종 취득세

        출처1 : https://hwanggum.tistory.com/335
        출처2 : http://xn--989a00af8jnslv3dba.com/%EC%B7%A8%EB%93%9D%EC%84%B8
        """
        if (
            not private_area
            or private_area == 0
            or not supply_price
            or supply_price == 0
        ):
            return 0

        if supply_price <= 60000:
            if private_area <= 85:
                tax_rate = 0.011
            else:
                tax_rate = 0.013
        elif 60000 < supply_price <= 90000:
            if private_area <= 85:
                tax_rate = (supply_price * 2 / 30000 - 3) * 0.01 * 1.1
            else:
                tax_rate = (supply_price * 2 / 30000 - 3) * 0.01 * 1.1 + 0.002
        else:
            if private_area <= 85:
                tax_rate = 0.033
            else:
                tax_rate = 0.035

        total_acquisition_tax = MathHelper.round(num=supply_price * tax_rate)

        return total_acquisition_tax

    def get_sub_ids(self, sub_details: list[SubDtToPublicDtEntity]) -> list[int]:
        sub_ids = list()
        for sub_detail in sub_details:
            sub_ids.append(sub_detail.subs_id)
        return sub_ids

    def _get_public_sale_detail_id(
        self,
        sub_detail: SubDtToPublicDtEntity,
        public_sale_details: list[PublicDtUniqueEntity],
    ) -> int:
        public_sale_detail_id = None
        for public_sale_detail in public_sale_details:
            area_type = self._get_area_type(sub_detail.area_type)
            private_area = self._get_private_area(sub_detail.area_type)
            if (
                public_sale_detail.area_type == area_type
                and public_sale_detail.private_area == private_area
            ):
                public_sale_detail_id = public_sale_detail.id
        return public_sale_detail_id

    def _get_region_percent(self, sub_detail: SubDtToPublicDtEntity) -> list[int]:
        if (
            sub_detail.supply_rate is not None
            and sub_detail.supply_rate_etc is not None
        ):
            supply_rate = int(sub_detail.supply_rate)
            supply_rate_etc = int(sub_detail.supply_rate_etc)
            supply_rate_gyeonggi = (
                100 - int(sub_detail.supply_rate) - int(sub_detail.supply_rate_etc)
            )
            return [supply_rate, supply_rate_gyeonggi, supply_rate_etc]

        elif sub_detail.housing_category == "민영":
            return [100, 0, 0]

        else:
            if sub_detail.region == "경기":
                return [30, 20, 50]
            else:
                return [50, 0, 50]
