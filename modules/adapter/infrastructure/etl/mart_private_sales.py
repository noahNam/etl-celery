from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    BasicInfoEntity,
    CalcMgmtCostEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_model import (
    PrivateSaleModel,
)


class TransformPrivateSale:
    def start_etl(
        self,
        from_model: str,
        target_list: list[BasicInfoEntity],
        options: list[list[CalcMgmtCostEntity]] | None,
    ) -> list[PrivateSaleModel] | None:
        if not target_list:
            return None

        if from_model == "basic_infos":
            return self._etl_private_sales(basic_infos=target_list, mgmt_costs=options)

    def _etl_private_sales(
        self,
        basic_infos: list[BasicInfoEntity],
        mgmt_costs: list[CalcMgmtCostEntity] | None,
    ) -> list[PrivateSaleModel]:

        manage_cost_results = dict()
        summer_months = ["07", "08"]
        winter_months = ["01", "02"]

        for mgmt_cost_list in mgmt_costs:
            # 관리비 계산
            house_id = None
            summer_manage_cost = 0
            winter_manage_cost = 0
            avg_manage_cost = 0
            summer_usage_cnt = 0
            winter_usage_cnt = 0
            avg_usage_cnt = 0

            for mgmt_cost in mgmt_cost_list:
                house_id = mgmt_cost.house_id

                if not mgmt_cost.is_available or not mgmt_cost.priv_area:
                    continue

                # 아래 조건이 충족되면 다음 house_id로 넘김
                if (
                    summer_usage_cnt >= 2
                    and winter_usage_cnt >= 2
                    and avg_usage_cnt >= 12
                ):
                    continue

                payment_month = mgmt_cost.payment_date[-2:]

                # (공용관리비계 + 개별사용료계 + 장충금월부과금 - 잡수익월수입금액) / 단지주거전용면적(priv_area) = 관리비(m2당)
                total_manage_cost = (
                    mgmt_cost.common_manage_cost
                    + mgmt_cost.individual_fee
                    + mgmt_cost.public_part_imp_cost
                    - mgmt_cost.etc_income_amount
                ) / mgmt_cost.priv_area

                # 여름 관리비
                if payment_month in summer_months and (
                    summer_usage_cnt >= 0 and summer_usage_cnt < 2
                ):
                    # payment_date가 2022년7월 다음 payment_date가 2021년8월이면 최근 년도 기준으로 보여주기 위한 조건
                    if not summer_usage_cnt and payment_month == "07":
                        summer_usage_cnt = -1
                    else:
                        summer_usage_cnt += 1

                    summer_manage_cost += total_manage_cost

                # 겨울 관리비
                if payment_month in winter_months and (
                    winter_usage_cnt >= 0 and winter_usage_cnt < 2
                ):
                    # payment_date가 2022년1월 다음 payment_date가 2021년2월이면 최근 년도 기준으로 보여주기 위한 조건
                    if not winter_usage_cnt and payment_month == "01":
                        winter_usage_cnt = -1
                    else:
                        winter_usage_cnt += 1

                    winter_manage_cost += total_manage_cost

                # 최근 1년 평균 관리비
                if avg_usage_cnt < 12:
                    avg_usage_cnt += 1
                    avg_manage_cost += total_manage_cost

            if house_id:
                manage_cost_results.update(  # PrivateSaleModel에서 사용할 value 담는 dict
                    {
                        house_id: [
                            summer_manage_cost / abs(summer_usage_cnt) if summer_usage_cnt else None,
                            winter_manage_cost / abs(winter_usage_cnt) if winter_usage_cnt else None,
                            avg_manage_cost / avg_usage_cnt  if avg_usage_cnt else None,
                        ]
                    }
                )

        result = list()
        for basic_info in basic_infos:
            manage_cost_result = (
                manage_cost_results.get(basic_info.house_id)
                if manage_cost_results
                else None
            )
            result.append(
                PrivateSaleModel(
                    id=basic_info.house_id,
                    real_estate_id=basic_info.place_id,
                    name=basic_info.bld_name,
                    building_type=basic_info.code_apt_nm,
                    build_year=basic_info.use_apr_day,
                    move_in_date=basic_info.use_apr_day,
                    dong_cnt=basic_info.dong_cnt,
                    hhld_cnt=basic_info.hhld_cnt,
                    heat_type=basic_info.heat_type,
                    hallway_type=basic_info.hallway_type,
                    builder=basic_info.builder,
                    park_total_cnt=basic_info.park_total_cnt,
                    park_ground_cnt=basic_info.park_ground_cnt,
                    park_underground_cnt=basic_info.park_underground_cnt,
                    cctv_cnt=basic_info.cctv_cnt,
                    welfare=basic_info.welfare,
                    vl_rat=basic_info.vl_rat,
                    bc_rat=basic_info.bc_rat,
                    summer_mgmt_cost=manage_cost_result[0]
                    if manage_cost_result
                    else None,
                    winter_mgmt_cost=manage_cost_result[1]
                    if manage_cost_result
                    else None,
                    avg_mgmt_cost=manage_cost_result[2] if manage_cost_result else None,
                    public_ref_id=basic_info.public_ref_id,
                    rebuild_ref_id=basic_info.rebuild_ref_id,
                    is_available=basic_info.is_available,
                )
            )
        return result
