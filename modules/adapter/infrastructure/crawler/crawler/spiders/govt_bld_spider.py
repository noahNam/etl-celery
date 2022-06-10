from scrapy import Spider, Request
from xmltodict import parse

from modules.adapter.infrastructure.crawler.crawler.enum.govt_bld_enum import (
    GovtBldEnum,
)
from modules.adapter.infrastructure.crawler.crawler.items import (
    GovtBldInputInfo,
    GovtBldTopInfoItem,
    GovtBldMidInfoItem,
    GovtBldAreaInfoItem,
)
from modules.adapter.infrastructure.pypubsub.enum.call_failure_history_enum import (
    CallFailureTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.event_listener import event_listener_dict
from modules.adapter.infrastructure.pypubsub.event_observer import send_message
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    GovtBldInputEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.call_failure_history_model import (
    CallFailureHistoryModel,
)


class GovtBldSpider(Spider):
    name = "govt_bld_infos"
    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         "modules.adapter.infrastructure.crawler.crawler.pipelines.GovtBldPipeline": 300
    #     },
    # }
    open_api_service_key = GovtBldEnum.SERVICE_KEY_1.value
    request_count: int = 0

    def start_requests(self):
        """self.params : list[KaptOpenApiInputEntity] from KaptOpenApiUseCase class"""

        urls: list = [
            GovtBldEnum.GOVT_BLD_TOP_URL.value,
            GovtBldEnum.GOVT_BLD_MID_URL.value,
            GovtBldEnum.GOVT_BLD_AREA_URL.value,
        ]

        # 번지 추출
        input_params: list[GovtBldInputInfo] | None = self.get_input_infos(
            bld_info_list=self.params
        )

        if input_params:
            for param in input_params:
                yield Request(
                    url=urls[0] + f"?ServiceKey={GovtBldSpider.open_api_service_key}"
                    f"&sigunguCd={param.sigungu_code}"
                    f"&bjdongCd={param.bjdong_code}"
                    f"&platGbCd=0"
                    f"&bun={param.bun}"
                    f"&ji={param.ji}"
                    f"&numOfRows={GovtBldEnum.NUMBER_OF_ROWS.value}"
                    f"&pageNo=1",
                    callback=self.parse_bld_top_info,
                    errback=self.error_callback_bld_top_info,
                    meta={
                        "house_id": param.house_id,
                        "kapt_code": param.kapt_code,
                        "name": param.name,
                        "origin_dong_address": param.origin_dong_address,
                        "new_dong_address": param.new_dong_address,
                        "bjd_code": param.origin_bjd_code,
                        "url": urls[0]
                        + f"?kaptCode={param.kapt_code}&ServiceKey={GovtBldSpider.open_api_service_key}",
                    },
                )
                yield Request(
                    url=urls[1] + f"?ServiceKey={GovtBldSpider.open_api_service_key}"
                    f"&sigunguCd={param.sigungu_code}"
                    f"&bjdongCd={param.bjdong_code}"
                    f"&platGbCd=0"
                    f"&bun={param.bun}"
                    f"&ji={param.ji}"
                    f"&numOfRows={GovtBldEnum.NUMBER_OF_ROWS.value}"
                    f"&pageNo=1",
                    callback=self.parse_bld_mid_info,
                    errback=self.error_callback_bld_mid_info,
                    meta={
                        "house_id": param.house_id,
                        "kapt_code": param.kapt_code,
                        "name": param.name,
                        "origin_dong_address": param.origin_dong_address,
                        "new_dong_address": param.new_dong_address,
                        "bjd_code": param.origin_bjd_code,
                        "url": urls[0]
                        + f"?kaptCode={param.kapt_code}&ServiceKey={GovtBldSpider.open_api_service_key}",
                    },
                )
                yield Request(
                    url=urls[2] + f"?ServiceKey={GovtBldSpider.open_api_service_key}"
                    f"&sigunguCd={param.sigungu_code}"
                    f"&bjdongCd={param.bjdong_code}"
                    f"&platGbCd=0"
                    f"&bun={param.bun}"
                    f"&ji={param.ji}"
                    f"&numOfRows={GovtBldEnum.NUMBER_OF_ROWS.value}"
                    f"&pageNo=1",
                    callback=self.parse_bld_area_info,
                    errback=self.error_callback_bld_area_info,
                    meta={
                        "house_id": param.house_id,
                        "kapt_code": param.kapt_code,
                        "name": param.name,
                        "origin_dong_address": param.origin_dong_address,
                        "new_dong_address": param.new_dong_address,
                        "bjd_code": param.origin_bjd_code,
                        "url": urls[0]
                        + f"?kaptCode={param.kapt_code}&ServiceKey={GovtBldSpider.open_api_service_key}",
                    },
                )

    def parse_bld_top_info(self, response):
        xml_to_dict = parse(response.text)
        item: GovtBldTopInfoItem | None = None
        try:
            item: GovtBldTopInfoItem = GovtBldTopInfoItem(
                house_id=response.request.meta["house_id"],
                mgm_bldrgst_pk=xml_to_dict["response"]["body"]["item"].get(
                    "mgmBldrgstPk"
                ),
                itg_bld_grade=xml_to_dict["response"]["body"]["item"].get(
                    "itgBldGrade"
                ),
                itg_bld_cert=xml_to_dict["response"]["body"]["item"].get("itgBldCert"),
                crtn_day=xml_to_dict["response"]["body"]["item"].get("crtnDay"),
                na_bjdong_cd=xml_to_dict["response"]["body"]["item"].get("naBjdongCd"),
                na_ugrnd_cd=xml_to_dict["response"]["body"]["item"].get("naUgrndCd"),
                na_main_bun=xml_to_dict["response"]["body"]["item"].get("naMainBun"),
                na_sub_bun=xml_to_dict["response"]["body"]["item"].get("naSubBun"),
                plat_area=xml_to_dict["response"]["body"]["item"].get("platArea"),
                arch_area=xml_to_dict["response"]["body"]["item"].get("archArea"),
                bc_rat=xml_to_dict["response"]["body"]["item"].get("bcRat"),
                tot_area=xml_to_dict["response"]["body"]["item"].get("totArea"),
                vl_rat_estm_tot_area=xml_to_dict["response"]["body"]["item"].get(
                    "vlRatEstmTotArea"
                ),
                vl_rat=xml_to_dict["response"]["body"]["item"].get("vlRat"),
                main_purps_cd=xml_to_dict["response"]["body"]["item"].get(
                    "mainPurpsCd"
                ),
                main_purps_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "mainPurpsCdNm"
                ),
                etc_purps=xml_to_dict["response"]["body"]["item"].get("etcPurps"),
                hhld_cnt=xml_to_dict["response"]["body"]["item"].get("hhldCnt"),
                fmly_cnt=xml_to_dict["response"]["body"]["item"].get("fmlyCnt"),
                main_bld_cnt=xml_to_dict["response"]["body"]["item"].get("mainBldCnt"),
                atch_bld_cnt=xml_to_dict["response"]["body"]["item"].get("atchBldCnt"),
                atch_bld_area=xml_to_dict["response"]["body"]["item"].get(
                    "atchBldArea"
                ),
                tot_pkng_cnt=xml_to_dict["response"]["body"]["item"].get("totPkngCnt"),
                indr_mech_utcnt=xml_to_dict["response"]["body"]["item"].get(
                    "indrMechUtcnt"
                ),
                indr_mech_area=xml_to_dict["response"]["body"]["item"].get(
                    "indrMechArea"
                ),
                oudr_mech_utcnt=xml_to_dict["response"]["body"]["item"].get(
                    "oudrMechUtcnt"
                ),
                oudr_mech_area=xml_to_dict["response"]["body"]["item"].get(
                    "oudrMechArea"
                ),
                indr_auto_utcnt=xml_to_dict["response"]["body"]["item"].get(
                    "indrAutoUtcnt"
                ),
                indr_auto_area=xml_to_dict["response"]["body"]["item"].get(
                    "indrAutoArea"
                ),
                oudr_auto_utcnt=xml_to_dict["response"]["body"]["item"].get(
                    "oudrAutoUtcnt"
                ),
                oudr_auto_area=xml_to_dict["response"]["body"]["item"].get(
                    "oudrAutoArea"
                ),
                pms_day=xml_to_dict["response"]["body"]["item"].get("pmsDay"),
                stcns_day=xml_to_dict["response"]["body"]["item"].get("stcnsDay"),
                use_apr_day=xml_to_dict["response"]["body"]["item"].get("useAprDay"),
                pmsno_year=xml_to_dict["response"]["body"]["item"].get("pmsnoYear"),
                pmsno_kik_cd=xml_to_dict["response"]["body"]["item"].get("pmsnoKikCd"),
                pmsno_kik_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "pmsnoKikCdNm"
                ),
                pmsno_gb_cd=xml_to_dict["response"]["body"]["item"].get("pmsnoGbCd"),
                pmsno_gb_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "pmsnoGbCdNm"
                ),
                ho_cnt=xml_to_dict["response"]["body"]["item"].get("hoCnt"),
                engr_grade=xml_to_dict["response"]["body"]["item"].get("engrGrade"),
                engr_rat=xml_to_dict["response"]["body"]["item"].get("engrRat"),
                engr_epi=xml_to_dict["response"]["body"]["item"].get("engrEpi"),
                gn_bld_grade=xml_to_dict["response"]["body"]["item"].get("gnBldGrade"),
                gn_bld_cert=xml_to_dict["response"]["body"]["item"].get("gnBldCert"),
                rnum=xml_to_dict["response"]["body"]["item"].get("rnum"),
                plat_plc=xml_to_dict["response"]["body"]["item"].get("platPlc"),
                sigungu_cd=xml_to_dict["response"]["body"]["item"].get("sigunguCd"),
                bjdong_cd=xml_to_dict["response"]["body"]["item"].get("bjdongCd"),
                plat_gb_cd=xml_to_dict["response"]["body"]["item"].get("platGbCd"),
                bun=xml_to_dict["response"]["body"]["item"].get("bun"),
                ji=xml_to_dict["response"]["body"]["item"].get("ji"),
                regstr_gb_cd=xml_to_dict["response"]["body"]["item"].get("regstrGbCd"),
                regstr_gb_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "regstrGbCdNm"
                ),
                regstr_kind_cd=xml_to_dict["response"]["body"]["item"].get(
                    "regstrKindCd"
                ),
                regstr_kind_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "regstrKindCdNm"
                ),
                new_old_regstr_gb_cd=xml_to_dict["response"]["body"]["item"].get(
                    "newOldRegstrGbCd"
                ),
                new_old_regstr_gb_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "newOldRegstrGbCdNm"
                ),
                new_plat_plc=xml_to_dict["response"]["body"]["item"].get("newPlatPlc"),
                bld_nm=xml_to_dict["response"]["body"]["item"].get("bldNm"),
                splot_nm=xml_to_dict["response"]["body"]["item"].get("splotNm"),
                block=xml_to_dict["response"]["body"]["item"].get("block"),
                lot=xml_to_dict["response"]["body"]["item"].get("lot"),
                bylot_cnt=xml_to_dict["response"]["body"]["item"].get("bylotCnt"),
                na_road_cd=xml_to_dict["response"]["body"]["item"].get("naRoadCd"),
            )
        except KeyError:
            pass

        self.count_requests()

        if item:
            yield item

    def parse_bld_mid_info(self, response):
        xml_to_dict = parse(response.text)
        item: GovtBldMidInfoItem | None = None

        try:
            item: GovtBldMidInfoItem = GovtBldMidInfoItem(
                house_id=response.request.meta["house_id"],
                mgm_bldrgst_pk=xml_to_dict["response"]["body"]["item"].get(
                    "mgmBldrgstPk"
                ),
                main_purps_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "mainPurpsCdNm"
                ),
                etc_purps=xml_to_dict["response"]["body"]["item"].get("etcPurps"),
                roof_cd=xml_to_dict["response"]["body"]["item"].get("roofCd"),
                roof_cd_nm=xml_to_dict["response"]["body"]["item"].get("roofCdNm"),
                etc_roof=xml_to_dict["response"]["body"]["item"].get("etcRoof"),
                hhld_cnt=xml_to_dict["response"]["body"]["item"].get("hhldCnt"),
                fmly_cnt=xml_to_dict["response"]["body"]["item"].get("fmlyCnt"),
                heit=xml_to_dict["response"]["body"]["item"].get("heit"),
                grnd_flr_cnt=xml_to_dict["response"]["body"]["item"].get("grndFlrCnt"),
                ugrnd_flr_cnt=xml_to_dict["response"]["body"]["item"].get(
                    "ugrndFlrCnt"
                ),
                ride_use_elvt_cnt=xml_to_dict["response"]["body"]["item"].get(
                    "rideUseElvtCnt"
                ),
                emgen_use_elvt_cnt=xml_to_dict["response"]["body"]["item"].get(
                    "emgenUseElvtCnt"
                ),
                atch_bld_cnt=xml_to_dict["response"]["body"]["item"].get("atchBldCnt"),
                atch_bld_area=xml_to_dict["response"]["body"]["item"].get(
                    "atchBldArea"
                ),
                tot_dong_tot_area=xml_to_dict["response"]["body"]["item"].get(
                    "totDongTotArea"
                ),
                indr_mech_utcnt=xml_to_dict["response"]["body"]["item"].get(
                    "indrMechUtcnt"
                ),
                indr_mech_area=xml_to_dict["response"]["body"]["item"].get(
                    "indrMechArea"
                ),
                oudr_mech_utcnt=xml_to_dict["response"]["body"]["item"].get(
                    "oudrMechUtcnt"
                ),
                oudr_mech_area=xml_to_dict["response"]["body"]["item"].get(
                    "oudrMechArea"
                ),
                indr_auto_utcnt=xml_to_dict["response"]["body"]["item"].get(
                    "indrAutoUtcnt"
                ),
                indr_auto_area=xml_to_dict["response"]["body"]["item"].get(
                    "indrAutoArea"
                ),
                oudr_auto_utcnt=xml_to_dict["response"]["body"]["item"].get(
                    "oudrAutoUtcnt"
                ),
                oudr_auto_area=xml_to_dict["response"]["body"]["item"].get(
                    "oudrAutoArea"
                ),
                pms_day=xml_to_dict["response"]["body"]["item"].get("pmsDay"),
                stcns_day=xml_to_dict["response"]["body"]["item"].get("stcnsDay"),
                use_apr_day=xml_to_dict["response"]["body"]["item"].get("useAprDay"),
                pmsno_year=xml_to_dict["response"]["body"]["item"].get("pmsnoYear"),
                pmsno_kik_cd=xml_to_dict["response"]["body"]["item"].get("pmsnoKikCd"),
                pmsno_kik_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "pmsnoKikCdNm"
                ),
                pmsno_gb_cd=xml_to_dict["response"]["body"]["item"].get("pmsnoGbCd"),
                pmsno_gb_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "pmsnoGbCdNm"
                ),
                ho_cnt=xml_to_dict["response"]["body"]["item"].get("hoCnt"),
                engr_grade=xml_to_dict["response"]["body"]["item"].get("engrGrade"),
                engr_rat=xml_to_dict["response"]["body"]["item"].get("engrRat"),
                engr_epi=xml_to_dict["response"]["body"]["item"].get("engrEpi"),
                gn_bld_grade=xml_to_dict["response"]["body"]["item"].get("gnBldGrade"),
                gn_bld_cert=xml_to_dict["response"]["body"]["item"].get("gnBldCert"),
                itg_bld_grade=xml_to_dict["response"]["body"]["item"].get(
                    "itgBldGrade"
                ),
                itg_bld_cert=xml_to_dict["response"]["body"]["item"].get("itgBldCert"),
                crtn_day=xml_to_dict["response"]["body"]["item"].get("crtnDay"),
                rnum=xml_to_dict["response"]["body"]["item"].get("rnum"),
                plat_plc=xml_to_dict["response"]["body"]["item"].get("platPlc"),
                sigungu_cd=xml_to_dict["response"]["body"]["item"].get("sigunguCd"),
                bjdong_cd=xml_to_dict["response"]["body"]["item"].get("bjdongCd"),
                plat_gb_cd=xml_to_dict["response"]["body"]["item"].get("platGbCd"),
                bun=xml_to_dict["response"]["body"]["item"].get("bun"),
                ji=xml_to_dict["response"]["body"]["item"].get("ji"),
                regstr_gb_cd=xml_to_dict["response"]["body"]["item"].get("regstrGbCd"),
                regstr_gb_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "regstrGbCdNm"
                ),
                regstr_kind_cd=xml_to_dict["response"]["body"]["item"].get(
                    "regstrKindCd"
                ),
                regstr_kind_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "regstrKindCdNm"
                ),
                new_plat_plc=xml_to_dict["response"]["body"]["item"].get("newPlatPlc"),
                bld_nm=xml_to_dict["response"]["body"]["item"].get("bldNm"),
                splot_nm=xml_to_dict["response"]["body"]["item"].get("splotNm"),
                block=xml_to_dict["response"]["body"]["item"].get("block"),
                lot=xml_to_dict["response"]["body"]["item"].get("lot"),
                bylot_cnt=xml_to_dict["response"]["body"]["item"].get("bylotCnt"),
                na_road_cd=xml_to_dict["response"]["body"]["item"].get("naRoadCd"),
                na_bjdong_cd=xml_to_dict["response"]["body"]["item"].get("naBjdongCd"),
                na_ugrnd_cd=xml_to_dict["response"]["body"]["item"].get("naUgrndCd"),
                na_main_bun=xml_to_dict["response"]["body"]["item"].get("naMainBun"),
                na_sub_bun=xml_to_dict["response"]["body"]["item"].get("naSubBun"),
                dong_nm=xml_to_dict["response"]["body"]["item"].get("dongNm"),
                main_atch_gb_cd=xml_to_dict["response"]["body"]["item"].get(
                    "mainAtchGbCd"
                ),
                main_atch_gb_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "mainAtchGbCdNm"
                ),
                plat_area=xml_to_dict["response"]["body"]["item"].get("platArea"),
                arch_area=xml_to_dict["response"]["body"]["item"].get("archArea"),
                bc_rat=xml_to_dict["response"]["body"]["item"].get("bcRat"),
                tot_area=xml_to_dict["response"]["body"]["item"].get("totArea"),
                vl_rat_estm_tot_area=xml_to_dict["response"]["body"]["item"].get(
                    "vlRatEstmTotArea"
                ),
                vl_rat=xml_to_dict["response"]["body"]["item"].get("vlRat"),
                strct_cd=xml_to_dict["response"]["body"]["item"].get("strctCd"),
                strct_cd_nm=xml_to_dict["response"]["body"]["item"].get("strctCdNm"),
                etc_strct=xml_to_dict["response"]["body"]["item"].get("etcStrct"),
                main_purps_cd=xml_to_dict["response"]["body"]["item"].get(
                    "mainPurpsCd"
                ),
                rserthqk_dsgn_apply_yn=xml_to_dict["response"]["body"]["item"].get(
                    "rserthqkDsgnApplyYn"
                ),
                rserthqk_ablty=xml_to_dict["response"]["body"]["item"].get(
                    "rserthqkAblty"
                ),
            )
        except KeyError:
            pass

        self.count_requests()

        if item:
            yield item

    def parse_bld_area_info(self, response):
        xml_to_dict = parse(response.text)
        item: GovtBldAreaInfoItem | None = None

        try:
            item: GovtBldAreaInfoItem = GovtBldAreaInfoItem(
                house_id=response.request.meta["house_id"],
                mgm_bldrgst_pk=xml_to_dict["response"]["body"]["item"].get(
                    "mgmBldrgstPk"
                ),
                regstr_gb_cd=xml_to_dict["response"]["body"]["item"].get("regstrGbCd"),
                regstr_gb_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "regstrGbCdNm"
                ),
                regstr_kind_cd=xml_to_dict["response"]["body"]["item"].get(
                    "regstrKindCd"
                ),
                regstr_kind_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "regstrKindCdNm"
                ),
                new_plat_plc=xml_to_dict["response"]["body"]["item"].get("newPlatPlc"),
                bld_nm=xml_to_dict["response"]["body"]["item"].get("bldNm"),
                splot_nm=xml_to_dict["response"]["body"]["item"].get("splotNm"),
                block=xml_to_dict["response"]["body"]["item"].get("block"),
                lot=xml_to_dict["response"]["body"]["item"].get("lot"),
                bylot_cnt=xml_to_dict["response"]["body"]["item"].get("bylotCnt"),
                na_road_cd=xml_to_dict["response"]["body"]["item"].get("naRoadCd"),
                na_bjdong_cd=xml_to_dict["response"]["body"]["item"].get("naBjdongCd"),
                na_ugrnd_cd=xml_to_dict["response"]["body"]["item"].get("naUgrndCd"),
                na_main_bun=xml_to_dict["response"]["body"]["item"].get("naMainBun"),
                na_sub_bun=xml_to_dict["response"]["body"]["item"].get("naSubBun"),
                dong_nm=xml_to_dict["response"]["body"]["item"].get("dongNm"),
                ho_nm=xml_to_dict["response"]["body"]["item"].get("hoNm"),
                flr_gb_cd=xml_to_dict["response"]["body"]["item"].get("flrGbCd"),
                flr_gb_cd_nm=xml_to_dict["response"]["body"]["item"].get("flrGbCdNm"),
                flr_no=xml_to_dict["response"]["body"]["item"].get("flrNo"),
                flr_no_nm=xml_to_dict["response"]["body"]["item"].get("flrNoNm"),
                expos_pubuse_gb_cd=xml_to_dict["response"]["body"]["item"].get(
                    "exposPubuseGbCd"
                ),
                expos_pubuse_gb_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "exposPubuseGbCdNm"
                ),
                main_atch_gb_cd=xml_to_dict["response"]["body"]["item"].get(
                    "mainAtchGbCd"
                ),
                main_atch_gb_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "mainAtchGbCdNm"
                ),
                strct_cd=xml_to_dict["response"]["body"]["item"].get("strctCd"),
                strct_cd_nm=xml_to_dict["response"]["body"]["item"].get("strctCdNm"),
                etc_strct=xml_to_dict["response"]["body"]["item"].get("etcStrct"),
                main_purps_cd=xml_to_dict["response"]["body"]["item"].get(
                    "mainPurpsCd"
                ),
                main_purps_cd_nm=xml_to_dict["response"]["body"]["item"].get(
                    "mainPurpsCdNm"
                ),
                etc_purps=xml_to_dict["response"]["body"]["item"].get("etcPurps"),
                area=xml_to_dict["response"]["body"]["item"].get("area"),
                crtn_day=xml_to_dict["response"]["body"]["item"].get("crtnDay"),
                rnum=xml_to_dict["response"]["body"]["item"].get("rnum"),
                plat_plc=xml_to_dict["response"]["body"]["item"].get("platPlc"),
                sigungu_cd=xml_to_dict["response"]["body"]["item"].get("sigunguCd"),
                bjdong_cd=xml_to_dict["response"]["body"]["item"].get("bjdongCd"),
                plat_gb_cd=xml_to_dict["response"]["body"]["item"].get("platGbCd"),
                bun=xml_to_dict["response"]["body"]["item"].get("bun"),
                ji=xml_to_dict["response"]["body"]["item"].get("ji"),
            )
        except KeyError:
            pass

        self.count_requests()

        if item:
            yield item

    def error_callback_bld_top_info(self, failure):
        self.save_failure_info(
            ref_table="govt_bld_top_infos",
            current_house_id=failure.request.meta["house_id"],
            current_kapt_code=failure.request.meta["kapt_code"],
            current_bld_name=failure.request.meta["name"],
            new_dong_address=failure.request.meta["new_dong_address"],
            origin_dong_address=failure.request.meta["origin_dong_address"],
            bjd_code=failure.request.meta["bjd_code"],
            current_url=failure.request.meta["url"],
            response=failure,
        )

    def error_callback_bld_mid_info(self, failure):
        self.save_failure_info(
            ref_table="govt_bld_middle_infos",
            current_house_id=failure.request.meta["house_id"],
            current_kapt_code=failure.request.meta["kapt_code"],
            current_bld_name=failure.request.meta["name"],
            new_dong_address=failure.request.meta["new_dong_address"],
            origin_dong_address=failure.request.meta["origin_dong_address"],
            bjd_code=failure.request.meta["bjd_code"],
            current_url=failure.request.meta["url"],
            response=failure,
        )

    def error_callback_bld_area_info(self, failure):
        self.save_failure_info(
            ref_table="govt_bld_area_infos",
            current_house_id=failure.request.meta["house_id"],
            current_kapt_code=failure.request.meta["kapt_code"],
            current_bld_name=failure.request.meta["name"],
            new_dong_address=failure.request.meta["new_dong_address"],
            origin_dong_address=failure.request.meta["origin_dong_address"],
            bjd_code=failure.request.meta["bjd_code"],
            current_url=failure.request.meta["url"],
            response=failure,
        )

    def get_input_infos(
        self, bld_info_list: list[GovtBldInputEntity]
    ) -> list[GovtBldInputInfo] | None:
        input_infos: list[GovtBldInputInfo] | None = None
        for elm in bld_info_list:
            input_infos.append(self._extract_input_params(bld_info=elm))

        return input_infos

    def _extract_input_params(self, bld_info: GovtBldInputEntity) -> GovtBldInputInfo:
        """'0000' : 공공데이터 번지 파라미터 default value format"""
        bunji, bun, ji = None, "0000", "0000"

        if bld_info.new_dong_address:
            bunji = bld_info.new_dong_address.split(" ")[-1]
        else:
            bunji = bld_info.origin_dong_address.split(" ")[-1]

        if bunji:
            if "-" in bunji:
                bun = bun[len(bunji.split("-")[0]) :] + bunji.split("-")[0]
                ji = ji[len(bunji.split("-")[-1]) :] + bunji.split("-")[-1]
            else:
                bun = bun[len(bunji.split("-")[0]) :] + bunji.split("-")[0]

        return GovtBldInputInfo(
            house_id=bld_info.house_id,
            kapt_code=bld_info.kapt_code,
            name=bld_info.name,
            origin_dong_address=bld_info.origin_dong_address,
            new_dong_address=bld_info.new_dong_address,
            origin_bjd_code=bld_info.bjd_code,
            bun=bun,
            ji=ji,
            sigungu_code=bld_info.bjd_code[:5],
            bjdong_code=bld_info.bjd_code[5:],
        )

    def change_service_key(self):
        if GovtBldSpider.open_api_service_key == GovtBldEnum.SERVICE_KEY_2.value:
            GovtBldSpider.open_api_service_key = GovtBldEnum.SERVICE_KEY_1.value
        else:
            GovtBldSpider.open_api_service_key = GovtBldEnum.SERVICE_KEY_2.value

    def count_requests(self):
        if GovtBldSpider.request_count >= GovtBldEnum.DAILY_REQUEST_COUNT.value:
            self.change_service_key()
            GovtBldSpider.request_count = 0
        else:
            GovtBldSpider.request_count += 1

    def save_failure_info(
        self,
        ref_table,
        current_house_id,
        current_kapt_code,
        current_bld_name,
        new_dong_address,
        origin_dong_address,
        bjd_code,
        current_url,
        response,
    ) -> None:
        fail_orm: CallFailureHistoryModel = CallFailureHistoryModel(
            ref_id=current_house_id,
            ref_table=ref_table,
            param=f"url: {current_url}, "
            f"kapt_code: {current_kapt_code}, "
            f"current_bld_name: {current_bld_name}, "
            f"origin_dong_address: {origin_dong_address}, "
            f"new_dong_address: {new_dong_address}, "
            f"bjd_code: {bjd_code}",
            reason=f"response:{response.text}",
        )
        if not self.__is_exists_failure(fail_orm=fail_orm):
            self.__save_crawling_failure(fail_orm=fail_orm)

    def __save_crawling_failure(self, fail_orm: CallFailureHistoryModel) -> None:
        send_message(
            topic_name=CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value,
            fail_orm=fail_orm,
        )
        event_listener_dict.get(
            f"{CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value}", None
        )

    def __is_exists_failure(self, fail_orm: CallFailureHistoryModel | None) -> bool:
        send_message(
            topic_name=CallFailureTopicEnum.IS_EXISTS.value,
            fail_orm=fail_orm,
        )
        return event_listener_dict.get(f"{CallFailureTopicEnum.IS_EXISTS.value}")
