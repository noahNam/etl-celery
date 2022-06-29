import logging
import re

from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider
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
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)
logger.setLevel(logging.INFO)


class GovtBldSpider(Spider):
    name = "govt_bld_infos"
    custom_settings = {
        "ITEM_PIPELINES": {
            "modules.adapter.infrastructure.crawler.crawler.pipelines.GovtBldPipeline": 300
        },
    }
    open_api_service_key: str = GovtBldEnum.SERVICE_KEY_1.value

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
                    f"&bun={param.bun if param.bun else '0000'}"
                    f"&ji={param.ji if param.ji else '0000'}"
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
                        "bun:": param.bun if param.bun else "0000",
                        "ji:": param.ji if param.ji else "0000",
                        "url": urls[0]
                        + f"?ServiceKey={GovtBldSpider.open_api_service_key}"
                        f"&sigunguCd={param.sigungu_code}"
                        f"&bjdongCd={param.bjdong_code}"
                        f"&platGbCd=0"
                        f"&bun={param.bun if param.bun else '0000'}"
                        f"&ji={param.ji if param.ji else '0000'}"
                        f"&numOfRows={GovtBldEnum.NUMBER_OF_ROWS.value}"
                        f"&pageNo=1",
                    },
                )
                yield Request(
                    url=urls[1] + f"?ServiceKey={GovtBldSpider.open_api_service_key}"
                    f"&sigunguCd={param.sigungu_code}"
                    f"&bjdongCd={param.bjdong_code}"
                    f"&platGbCd=0"
                    f"&bun={param.bun if param.bun else '0000'}"
                    f"&ji={param.ji if param.ji else '0000'}"
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
                        "bun:": param.bun if param.bun else "0000",
                        "ji:": param.ji if param.ji else "0000",
                        "url": urls[1]
                        + f"?ServiceKey={GovtBldSpider.open_api_service_key}"
                        f"&sigunguCd={param.sigungu_code}"
                        f"&bjdongCd={param.bjdong_code}"
                        f"&platGbCd=0"
                        f"&bun={param.bun if param.bun else '0000'}"
                        f"&ji={param.ji if param.ji else '0000'}"
                        f"&numOfRows={GovtBldEnum.NUMBER_OF_ROWS.value}"
                        f"&pageNo=1",
                    },
                )
                yield Request(
                    url=urls[2] + f"?ServiceKey={GovtBldSpider.open_api_service_key}"
                    f"&sigunguCd={param.sigungu_code}"
                    f"&bjdongCd={param.bjdong_code}"
                    f"&platGbCd=0"
                    f"&bun={param.bun if param.bun else '0000'}"
                    f"&ji={param.ji if param.ji else '0000'}"
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
                        "bun:": param.bun if param.bun else "0000",
                        "ji:": param.ji if param.ji else "0000",
                        "url": urls[2]
                        + f"?ServiceKey={GovtBldSpider.open_api_service_key}"
                        f"&sigunguCd={param.sigungu_code}"
                        f"&bjdongCd={param.bjdong_code}"
                        f"&platGbCd=0"
                        f"&bun={param.bun if param.bun else '0000'}"
                        f"&ji={param.ji if param.ji else '0000'}"
                        f"&numOfRows={GovtBldEnum.NUMBER_OF_ROWS.value}"
                        f"&pageNo=1",
                    },
                )

    def is_need_to_change_service_key(self, xml_to_dict: dict) -> bool:
        if (
            "EXCEEDS" in xml_to_dict["response"]["header"].get("resultMsg")
            or "EXPIRED" in xml_to_dict["response"]["header"].get("resultMsg")
        ) and xml_to_dict["response"]["header"].get("resultMsg") != "NORMAL SERVICE.":
            return True
        return False

    def parse_bld_top_info(self, response):
        xml_to_dict = parse(response.text)
        item: GovtBldTopInfoItem | None = None

        if self.is_need_to_change_service_key(xml_to_dict=xml_to_dict):
            self.save_failure_info(
                ref_table="govt_bld_top_infos",
                current_house_id=response.request.meta.get("house_id"),
                current_kapt_code=response.request.meta.get("kapt_code"),
                current_bld_name=response.request.meta.get("name"),
                new_dong_address=response.request.meta.get("new_dong_address"),
                origin_dong_address=response.request.meta.get("origin_dong_address"),
                bjd_code=response.request.meta.get("bjd_code"),
                current_url=response.request.meta.get("url"),
                bun=response.request.meta.get("bun"),
                ji=response.request.meta.get("ji"),
                response_or_failure=response,
            )
            if not self._change_service_key():
                raise CloseSpider(
                    reason=f"[GovtBldSpider][parse_bld_top_info]: "
                    f"Daily Request Exceeds and All Service_key expired, Please try again later"
                )
            return None
        try:
            if isinstance(xml_to_dict["response"]["body"]["items"]["item"], list):
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
                for elm in xml_to_dict:
                    logger.info("@@@")
                    logger.info(f"찾은 갯수 : {len(xml_to_dict)}개")
                    item: GovtBldTopInfoItem = GovtBldTopInfoItem(
                        house_id=response.request.meta["house_id"],
                        mgm_bldrgst_pk=elm.get("mgmBldrgstPk"),
                        itg_bld_grade=elm.get("itgBldGrade"),
                        itg_bld_cert=elm.get("itgBldCert"),
                        crtn_day=elm.get("crtnDay"),
                        na_bjdong_cd=elm.get("naBjdongCd"),
                        na_ugrnd_cd=elm.get("naUgrndCd"),
                        na_main_bun=elm.get("naMainBun"),
                        na_sub_bun=elm.get("naSubBun"),
                        plat_area=elm.get("platArea"),
                        arch_area=elm.get("archArea"),
                        bc_rat=elm.get("bcRat"),
                        tot_area=elm.get("totArea"),
                        vl_rat_estm_tot_area=elm.get("vlRatEstmTotArea"),
                        vl_rat=elm.get("vlRat"),
                        main_purps_cd=elm.get("mainPurpsCd"),
                        main_purps_cd_nm=elm.get("mainPurpsCdNm"),
                        etc_purps=elm.get("etcPurps"),
                        hhld_cnt=elm.get("hhldCnt"),
                        fmly_cnt=elm.get("fmlyCnt"),
                        main_bld_cnt=elm.get("mainBldCnt"),
                        atch_bld_cnt=elm.get("atchBldCnt"),
                        atch_bld_area=elm.get("atchBldArea"),
                        tot_pkng_cnt=elm.get("totPkngCnt"),
                        indr_mech_utcnt=elm.get("indrMechUtcnt"),
                        indr_mech_area=elm.get("indrMechArea"),
                        oudr_mech_utcnt=elm.get("oudrMechUtcnt"),
                        oudr_mech_area=elm.get("oudrMechArea"),
                        indr_auto_utcnt=elm.get("indrAutoUtcnt"),
                        indr_auto_area=elm.get("indrAutoArea"),
                        oudr_auto_utcnt=elm.get("oudrAutoUtcnt"),
                        oudr_auto_area=elm.get("oudrAutoArea"),
                        pms_day=elm.get("pmsDay"),
                        stcns_day=elm.get("stcnsDay"),
                        use_apr_day=elm.get("useAprDay"),
                        pmsno_year=elm.get("pmsnoYear"),
                        pmsno_kik_cd=elm.get("pmsnoKikCd"),
                        pmsno_kik_cd_nm=elm.get("pmsnoKikCdNm"),
                        pmsno_gb_cd=elm.get("pmsnoGbCd"),
                        pmsno_gb_cd_nm=elm.get("pmsnoGbCdNm"),
                        ho_cnt=elm.get("hoCnt"),
                        engr_grade=elm.get("engrGrade"),
                        engr_rat=elm.get("engrRat"),
                        engr_epi=elm.get("engrEpi"),
                        gn_bld_grade=elm.get("gnBldGrade"),
                        gn_bld_cert=elm.get("gnBldCert"),
                        rnum=elm.get("rnum"),
                        plat_plc=elm.get("platPlc"),
                        sigungu_cd=elm.get("sigunguCd"),
                        bjdong_cd=elm.get("bjdongCd"),
                        plat_gb_cd=elm.get("platGbCd"),
                        bun=elm.get("bun"),
                        ji=elm.get("ji"),
                        regstr_gb_cd=elm.get("regstrGbCd"),
                        regstr_gb_cd_nm=elm.get("regstrGbCdNm"),
                        regstr_kind_cd=elm.get("regstrKindCd"),
                        regstr_kind_cd_nm=elm.get("regstrKindCdNm"),
                        new_old_regstr_gb_cd=elm.get("newOldRegstrGbCd"),
                        new_old_regstr_gb_cd_nm=elm.get("newOldRegstrGbCdNm"),
                        new_plat_plc=elm.get("newPlatPlc"),
                        bld_nm=elm.get("bldNm"),
                        splot_nm=elm.get("splotNm"),
                        block=elm.get("block"),
                        lot=elm.get("lot"),
                        bylot_cnt=elm.get("bylotCnt"),
                        na_road_cd=elm.get("naRoadCd"),
                    )
                    yield item
                return None

            elif not xml_to_dict["response"]["body"]["items"]:
                item = None
            else:
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
        except Exception:
            self.save_failure_info(
                ref_table="govt_bld_top_infos",
                current_house_id=response.request.meta.get("house_id"),
                current_kapt_code=response.request.meta.get("kapt_code"),
                current_bld_name=response.request.meta.get("name"),
                new_dong_address=response.request.meta.get("new_dong_address"),
                origin_dong_address=response.request.meta.get("origin_dong_address"),
                bjd_code=response.request.meta.get("bjd_code"),
                current_url=response.request.meta.get("url"),
                bun=response.request.meta.get("bun"),
                ji=response.request.meta.get("ji"),
                response_or_failure=response,
            )
            return None
        try:
            item: GovtBldTopInfoItem = GovtBldTopInfoItem(
                house_id=response.request.meta["house_id"],
                mgm_bldrgst_pk=xml_to_dict.get("mgmBldrgstPk"),
                itg_bld_grade=xml_to_dict.get("itgBldGrade"),
                itg_bld_cert=xml_to_dict.get("itgBldCert"),
                crtn_day=xml_to_dict.get("crtnDay"),
                na_bjdong_cd=xml_to_dict.get("naBjdongCd"),
                na_ugrnd_cd=xml_to_dict.get("naUgrndCd"),
                na_main_bun=xml_to_dict.get("naMainBun"),
                na_sub_bun=xml_to_dict.get("naSubBun"),
                plat_area=xml_to_dict.get("platArea"),
                arch_area=xml_to_dict.get("archArea"),
                bc_rat=xml_to_dict.get("bcRat"),
                tot_area=xml_to_dict.get("totArea"),
                vl_rat_estm_tot_area=xml_to_dict.get("vlRatEstmTotArea"),
                vl_rat=xml_to_dict.get("vlRat"),
                main_purps_cd=xml_to_dict.get("mainPurpsCd"),
                main_purps_cd_nm=xml_to_dict.get("mainPurpsCdNm"),
                etc_purps=xml_to_dict.get("etcPurps"),
                hhld_cnt=xml_to_dict.get("hhldCnt"),
                fmly_cnt=xml_to_dict.get("fmlyCnt"),
                main_bld_cnt=xml_to_dict.get("mainBldCnt"),
                atch_bld_cnt=xml_to_dict.get("atchBldCnt"),
                atch_bld_area=xml_to_dict.get("atchBldArea"),
                tot_pkng_cnt=xml_to_dict.get("totPkngCnt"),
                indr_mech_utcnt=xml_to_dict.get("indrMechUtcnt"),
                indr_mech_area=xml_to_dict.get("indrMechArea"),
                oudr_mech_utcnt=xml_to_dict.get("oudrMechUtcnt"),
                oudr_mech_area=xml_to_dict.get("oudrMechArea"),
                indr_auto_utcnt=xml_to_dict.get("indrAutoUtcnt"),
                indr_auto_area=xml_to_dict.get("indrAutoArea"),
                oudr_auto_utcnt=xml_to_dict.get("oudrAutoUtcnt"),
                oudr_auto_area=xml_to_dict.get("oudrAutoArea"),
                pms_day=xml_to_dict.get("pmsDay"),
                stcns_day=xml_to_dict.get("stcnsDay"),
                use_apr_day=xml_to_dict.get("useAprDay"),
                pmsno_year=xml_to_dict.get("pmsnoYear"),
                pmsno_kik_cd=xml_to_dict.get("pmsnoKikCd"),
                pmsno_kik_cd_nm=xml_to_dict.get("pmsnoKikCdNm"),
                pmsno_gb_cd=xml_to_dict.get("pmsnoGbCd"),
                pmsno_gb_cd_nm=xml_to_dict.get("pmsnoGbCdNm"),
                ho_cnt=xml_to_dict.get("hoCnt"),
                engr_grade=xml_to_dict.get("engrGrade"),
                engr_rat=xml_to_dict.get("engrRat"),
                engr_epi=xml_to_dict.get("engrEpi"),
                gn_bld_grade=xml_to_dict.get("gnBldGrade"),
                gn_bld_cert=xml_to_dict.get("gnBldCert"),
                rnum=xml_to_dict.get("rnum"),
                plat_plc=xml_to_dict.get("platPlc"),
                sigungu_cd=xml_to_dict.get("sigunguCd"),
                bjdong_cd=xml_to_dict.get("bjdongCd"),
                plat_gb_cd=xml_to_dict.get("platGbCd"),
                bun=xml_to_dict.get("bun"),
                ji=xml_to_dict.get("ji"),
                regstr_gb_cd=xml_to_dict.get("regstrGbCd"),
                regstr_gb_cd_nm=xml_to_dict.get("regstrGbCdNm"),
                regstr_kind_cd=xml_to_dict.get("regstrKindCd"),
                regstr_kind_cd_nm=xml_to_dict.get("regstrKindCdNm"),
                new_old_regstr_gb_cd=xml_to_dict.get("newOldRegstrGbCd"),
                new_old_regstr_gb_cd_nm=xml_to_dict.get("newOldRegstrGbCdNm"),
                new_plat_plc=xml_to_dict.get("newPlatPlc"),
                bld_nm=xml_to_dict.get("bldNm"),
                splot_nm=xml_to_dict.get("splotNm"),
                block=xml_to_dict.get("block"),
                lot=xml_to_dict.get("lot"),
                bylot_cnt=xml_to_dict.get("bylotCnt"),
                na_road_cd=xml_to_dict.get("naRoadCd"),
            )
        except KeyError:
            pass

        if item and item.mgm_bldrgst_pk:
            yield item
        else:
            self.save_failure_info(
                ref_table="govt_bld_top_infos",
                current_house_id=response.request.meta.get("house_id"),
                current_kapt_code=response.request.meta.get("kapt_code"),
                current_bld_name=response.request.meta.get("name"),
                new_dong_address=response.request.meta.get("new_dong_address"),
                origin_dong_address=response.request.meta.get("origin_dong_address"),
                bjd_code=response.request.meta.get("bjd_code"),
                current_url=response.request.meta.get("url"),
                bun=response.request.meta.get("bun"),
                ji=response.request.meta.get("ji"),
                response_or_failure=response,
            )

    def parse_bld_mid_info(self, response):
        xml_to_dict = parse(response.text)
        item: GovtBldMidInfoItem | None = None

        if self.is_need_to_change_service_key(xml_to_dict=xml_to_dict):
            self.save_failure_info(
                ref_table="govt_bld_middle_infos",
                current_house_id=response.request.meta.get("house_id"),
                current_kapt_code=response.request.meta.get("kapt_code"),
                current_bld_name=response.request.meta.get("name"),
                new_dong_address=response.request.meta.get("new_dong_address"),
                origin_dong_address=response.request.meta.get("origin_dong_address"),
                bjd_code=response.request.meta.get("bjd_code"),
                current_url=response.request.meta.get("url"),
                bun=response.request.meta.get("bun"),
                ji=response.request.meta.get("ji"),
                response_or_failure=response,
            )
            if not self._change_service_key():
                raise CloseSpider(
                    reason=f"[GovtBldSpider][parse_bld_mid_info]: "
                    f"Daily Request Exceeds and All Service_key expired, Please try again later"
                )
            return None
        try:
            if isinstance(xml_to_dict["response"]["body"]["items"]["item"], list):
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
                for elm in xml_to_dict:
                    item: GovtBldMidInfoItem = GovtBldMidInfoItem(
                        house_id=response.request.meta["house_id"],
                        mgm_bldrgst_pk=elm.get("mgmBldrgstPk"),
                        main_purps_cd_nm=elm.get("mainPurpsCdNm"),
                        etc_purps=elm.get("etcPurps"),
                        roof_cd=elm.get("roofCd"),
                        roof_cd_nm=elm.get("roofCdNm"),
                        etc_roof=elm.get("etcRoof"),
                        hhld_cnt=elm.get("hhldCnt"),
                        fmly_cnt=elm.get("fmlyCnt"),
                        heit=elm.get("heit"),
                        grnd_flr_cnt=elm.get("grndFlrCnt"),
                        ugrnd_flr_cnt=elm.get("ugrndFlrCnt"),
                        ride_use_elvt_cnt=elm.get("rideUseElvtCnt"),
                        emgen_use_elvt_cnt=elm.get("emgenUseElvtCnt"),
                        atch_bld_cnt=elm.get("atchBldCnt"),
                        atch_bld_area=elm.get("atchBldArea"),
                        tot_dong_tot_area=elm.get("totDongTotArea"),
                        indr_mech_utcnt=elm.get("indrMechUtcnt"),
                        indr_mech_area=elm.get("indrMechArea"),
                        oudr_mech_utcnt=elm.get("oudrMechUtcnt"),
                        oudr_mech_area=elm.get("oudrMechArea"),
                        indr_auto_utcnt=elm.get("indrAutoUtcnt"),
                        indr_auto_area=elm.get("indrAutoArea"),
                        oudr_auto_utcnt=elm.get("oudrAutoUtcnt"),
                        oudr_auto_area=elm.get("oudrAutoArea"),
                        pms_day=elm.get("pmsDay"),
                        stcns_day=elm.get("stcnsDay"),
                        use_apr_day=elm.get("useAprDay"),
                        pmsno_year=elm.get("pmsnoYear"),
                        pmsno_kik_cd=elm.get("pmsnoKikCd"),
                        pmsno_kik_cd_nm=elm.get("pmsnoKikCdNm"),
                        pmsno_gb_cd=elm.get("pmsnoGbCd"),
                        pmsno_gb_cd_nm=elm.get("pmsnoGbCdNm"),
                        ho_cnt=elm.get("hoCnt"),
                        engr_grade=elm.get("engrGrade"),
                        engr_rat=elm.get("engrRat"),
                        engr_epi=elm.get("engrEpi"),
                        gn_bld_grade=elm.get("gnBldGrade"),
                        gn_bld_cert=elm.get("gnBldCert"),
                        itg_bld_grade=elm.get("itgBldGrade"),
                        itg_bld_cert=elm.get("itgBldCert"),
                        crtn_day=elm.get("crtnDay"),
                        rnum=elm.get("rnum"),
                        plat_plc=elm.get("platPlc"),
                        sigungu_cd=elm.get("sigunguCd"),
                        bjdong_cd=elm.get("bjdongCd"),
                        plat_gb_cd=elm.get("platGbCd"),
                        bun=elm.get("bun"),
                        ji=elm.get("ji"),
                        regstr_gb_cd=elm.get("regstrGbCd"),
                        regstr_gb_cd_nm=elm.get("regstrGbCdNm"),
                        regstr_kind_cd=elm.get("regstrKindCd"),
                        regstr_kind_cd_nm=elm.get("regstrKindCdNm"),
                        new_plat_plc=elm.get("newPlatPlc"),
                        bld_nm=elm.get("bldNm"),
                        splot_nm=elm.get("splotNm"),
                        block=elm.get("block"),
                        lot=elm.get("lot"),
                        bylot_cnt=elm.get("bylotCnt"),
                        na_road_cd=elm.get("naRoadCd"),
                        na_bjdong_cd=elm.get("naBjdongCd"),
                        na_ugrnd_cd=elm.get("naUgrndCd"),
                        na_main_bun=elm.get("naMainBun"),
                        na_sub_bun=elm.get("naSubBun"),
                        dong_nm=elm.get("dongNm"),
                        main_atch_gb_cd=elm.get("mainAtchGbCd"),
                        main_atch_gb_cd_nm=elm.get("mainAtchGbCdNm"),
                        plat_area=elm.get("platArea"),
                        arch_area=elm.get("archArea"),
                        bc_rat=elm.get("bcRat"),
                        tot_area=elm.get("totArea"),
                        vl_rat_estm_tot_area=elm.get("vlRatEstmTotArea"),
                        vl_rat=elm.get("vlRat"),
                        strct_cd=elm.get("strctCd"),
                        strct_cd_nm=elm.get("strctCdNm"),
                        etc_strct=elm.get("etcStrct"),
                        main_purps_cd=elm.get("mainPurpsCd"),
                        rserthqk_dsgn_apply_yn=elm.get("rserthqkDsgnApplyYn"),
                        rserthqk_ablty=elm.get("rserthqkAblty"),
                    )
                    yield item
                return None

            elif not xml_to_dict["response"]["body"]["items"]:
                item = None
            else:
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
        except Exception:
            self.save_failure_info(
                ref_table="govt_bld_middle_infos",
                current_house_id=response.request.meta.get("house_id"),
                current_kapt_code=response.request.meta.get("kapt_code"),
                current_bld_name=response.request.meta.get("name"),
                new_dong_address=response.request.meta.get("new_dong_address"),
                origin_dong_address=response.request.meta.get("origin_dong_address"),
                bjd_code=response.request.meta.get("bjd_code"),
                current_url=response.request.meta.get("url"),
                bun=response.request.meta.get("bun"),
                ji=response.request.meta.get("ji"),
                response_or_failure=response,
            )

        try:
            item: GovtBldMidInfoItem = GovtBldMidInfoItem(
                house_id=response.request.meta["house_id"],
                mgm_bldrgst_pk=xml_to_dict.get("mgmBldrgstPk"),
                main_purps_cd_nm=xml_to_dict.get("mainPurpsCdNm"),
                etc_purps=xml_to_dict.get("etcPurps"),
                roof_cd=xml_to_dict.get("roofCd"),
                roof_cd_nm=xml_to_dict.get("roofCdNm"),
                etc_roof=xml_to_dict.get("etcRoof"),
                hhld_cnt=xml_to_dict.get("hhldCnt"),
                fmly_cnt=xml_to_dict.get("fmlyCnt"),
                heit=xml_to_dict.get("heit"),
                grnd_flr_cnt=xml_to_dict.get("grndFlrCnt"),
                ugrnd_flr_cnt=xml_to_dict.get("ugrndFlrCnt"),
                ride_use_elvt_cnt=xml_to_dict.get("rideUseElvtCnt"),
                emgen_use_elvt_cnt=xml_to_dict.get("emgenUseElvtCnt"),
                atch_bld_cnt=xml_to_dict.get("atchBldCnt"),
                atch_bld_area=xml_to_dict.get("atchBldArea"),
                tot_dong_tot_area=xml_to_dict.get("totDongTotArea"),
                indr_mech_utcnt=xml_to_dict.get("indrMechUtcnt"),
                indr_mech_area=xml_to_dict.get("indrMechArea"),
                oudr_mech_utcnt=xml_to_dict.get("oudrMechUtcnt"),
                oudr_mech_area=xml_to_dict.get("oudrMechArea"),
                indr_auto_utcnt=xml_to_dict.get("indrAutoUtcnt"),
                indr_auto_area=xml_to_dict.get("indrAutoArea"),
                oudr_auto_utcnt=xml_to_dict.get("oudrAutoUtcnt"),
                oudr_auto_area=xml_to_dict.get("oudrAutoArea"),
                pms_day=xml_to_dict.get("pmsDay"),
                stcns_day=xml_to_dict.get("stcnsDay"),
                use_apr_day=xml_to_dict.get("useAprDay"),
                pmsno_year=xml_to_dict.get("pmsnoYear"),
                pmsno_kik_cd=xml_to_dict.get("pmsnoKikCd"),
                pmsno_kik_cd_nm=xml_to_dict.get("pmsnoKikCdNm"),
                pmsno_gb_cd=xml_to_dict.get("pmsnoGbCd"),
                pmsno_gb_cd_nm=xml_to_dict.get("pmsnoGbCdNm"),
                ho_cnt=xml_to_dict.get("hoCnt"),
                engr_grade=xml_to_dict.get("engrGrade"),
                engr_rat=xml_to_dict.get("engrRat"),
                engr_epi=xml_to_dict.get("engrEpi"),
                gn_bld_grade=xml_to_dict.get("gnBldGrade"),
                gn_bld_cert=xml_to_dict.get("gnBldCert"),
                itg_bld_grade=xml_to_dict.get("itgBldGrade"),
                itg_bld_cert=xml_to_dict.get("itgBldCert"),
                crtn_day=xml_to_dict.get("crtnDay"),
                rnum=xml_to_dict.get("rnum"),
                plat_plc=xml_to_dict.get("platPlc"),
                sigungu_cd=xml_to_dict.get("sigunguCd"),
                bjdong_cd=xml_to_dict.get("bjdongCd"),
                plat_gb_cd=xml_to_dict.get("platGbCd"),
                bun=xml_to_dict.get("bun"),
                ji=xml_to_dict.get("ji"),
                regstr_gb_cd=xml_to_dict.get("regstrGbCd"),
                regstr_gb_cd_nm=xml_to_dict.get("regstrGbCdNm"),
                regstr_kind_cd=xml_to_dict.get("regstrKindCd"),
                regstr_kind_cd_nm=xml_to_dict.get("regstrKindCdNm"),
                new_plat_plc=xml_to_dict.get("newPlatPlc"),
                bld_nm=xml_to_dict.get("bldNm"),
                splot_nm=xml_to_dict.get("splotNm"),
                block=xml_to_dict.get("block"),
                lot=xml_to_dict.get("lot"),
                bylot_cnt=xml_to_dict.get("bylotCnt"),
                na_road_cd=xml_to_dict.get("naRoadCd"),
                na_bjdong_cd=xml_to_dict.get("naBjdongCd"),
                na_ugrnd_cd=xml_to_dict.get("naUgrndCd"),
                na_main_bun=xml_to_dict.get("naMainBun"),
                na_sub_bun=xml_to_dict.get("naSubBun"),
                dong_nm=xml_to_dict.get("dongNm"),
                main_atch_gb_cd=xml_to_dict.get("mainAtchGbCd"),
                main_atch_gb_cd_nm=xml_to_dict.get("mainAtchGbCdNm"),
                plat_area=xml_to_dict.get("platArea"),
                arch_area=xml_to_dict.get("archArea"),
                bc_rat=xml_to_dict.get("bcRat"),
                tot_area=xml_to_dict.get("totArea"),
                vl_rat_estm_tot_area=xml_to_dict.get("vlRatEstmTotArea"),
                vl_rat=xml_to_dict.get("vlRat"),
                strct_cd=xml_to_dict.get("strctCd"),
                strct_cd_nm=xml_to_dict.get("strctCdNm"),
                etc_strct=xml_to_dict.get("etcStrct"),
                main_purps_cd=xml_to_dict.get("mainPurpsCd"),
                rserthqk_dsgn_apply_yn=xml_to_dict.get("rserthqkDsgnApplyYn"),
                rserthqk_ablty=xml_to_dict.get("rserthqkAblty"),
            )
        except KeyError:
            pass

        if item and item.mgm_bldrgst_pk:
            yield item
        else:
            self.save_failure_info(
                ref_table="govt_bld_middle_infos",
                current_house_id=response.request.meta.get("house_id"),
                current_kapt_code=response.request.meta.get("kapt_code"),
                current_bld_name=response.request.meta.get("name"),
                new_dong_address=response.request.meta.get("new_dong_address"),
                origin_dong_address=response.request.meta.get("origin_dong_address"),
                bjd_code=response.request.meta.get("bjd_code"),
                current_url=response.request.meta.get("url"),
                bun=response.request.meta.get("bun"),
                ji=response.request.meta.get("ji"),
                response_or_failure=response,
            )

    def parse_bld_area_info(self, response):
        xml_to_dict: dict = parse(response.text)
        item: GovtBldAreaInfoItem | None = None

        if self.is_need_to_change_service_key(xml_to_dict=xml_to_dict):
            self.save_failure_info(
                ref_table="govt_bld_area_infos",
                current_house_id=response.request.meta.get("house_id"),
                current_kapt_code=response.request.meta.get("kapt_code"),
                current_bld_name=response.request.meta.get("name"),
                new_dong_address=response.request.meta.get("new_dong_address"),
                origin_dong_address=response.request.meta.get("origin_dong_address"),
                bjd_code=response.request.meta.get("bjd_code"),
                current_url=response.request.meta.get("url"),
                bun=response.request.meta.get("bun"),
                ji=response.request.meta.get("ji"),
                response_or_failure=response,
            )
            if not self._change_service_key():
                raise CloseSpider(
                    reason=f"[GovtBldSpider][parse_bld_area_info]: "
                    f"Daily Request Exceeds and All Service_key expired, Please try again later"
                )
            return None

        try:
            if isinstance(xml_to_dict["response"]["body"]["items"]["item"], list):
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
                for elm in xml_to_dict:
                    item: GovtBldAreaInfoItem = GovtBldAreaInfoItem(
                        house_id=response.request.meta["house_id"],
                        mgm_bldrgst_pk=elm.get("mgmBldrgstPk"),
                        regstr_gb_cd=elm.get("regstrGbCd"),
                        regstr_gb_cd_nm=elm.get("regstrGbCdNm"),
                        regstr_kind_cd=elm.get("regstrKindCd"),
                        regstr_kind_cd_nm=elm.get("regstrKindCdNm"),
                        new_plat_plc=elm.get("newPlatPlc"),
                        bld_nm=elm.get("bldNm"),
                        splot_nm=elm.get("splotNm"),
                        block=elm.get("block"),
                        lot=elm.get("lot"),
                        bylot_cnt=elm.get("bylotCnt"),
                        na_road_cd=elm.get("naRoadCd"),
                        na_bjdong_cd=elm.get("naBjdongCd"),
                        na_ugrnd_cd=elm.get("naUgrndCd"),
                        na_main_bun=elm.get("naMainBun"),
                        na_sub_bun=elm.get("naSubBun"),
                        dong_nm=elm.get("dongNm"),
                        ho_nm=elm.get("hoNm"),
                        flr_gb_cd=elm.get("flrGbCd"),
                        flr_gb_cd_nm=elm.get("flrGbCdNm"),
                        flr_no=elm.get("flrNo"),
                        flr_no_nm=elm.get("flrNoNm"),
                        expos_pubuse_gb_cd=elm.get("exposPubuseGbCd"),
                        expos_pubuse_gb_cd_nm=elm.get("exposPubuseGbCdNm"),
                        main_atch_gb_cd=elm.get("mainAtchGbCd"),
                        main_atch_gb_cd_nm=elm.get("mainAtchGbCdNm"),
                        strct_cd=elm.get("strctCd"),
                        strct_cd_nm=elm.get("strctCdNm"),
                        etc_strct=elm.get("etcStrct"),
                        main_purps_cd=elm.get("mainPurpsCd"),
                        main_purps_cd_nm=elm.get("mainPurpsCdNm"),
                        etc_purps=elm.get("etcPurps"),
                        area=elm.get("area"),
                        crtn_day=elm.get("crtnDay"),
                        rnum=elm.get("rnum"),
                        plat_plc=elm.get("platPlc"),
                        sigungu_cd=elm.get("sigunguCd"),
                        bjdong_cd=elm.get("bjdongCd"),
                        plat_gb_cd=elm.get("platGbCd"),
                        bun=elm.get("bun"),
                        ji=elm.get("ji"),
                    )
                    yield item
                return None

            elif not xml_to_dict["response"]["body"]["items"]:
                item = None
            else:
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
        except Exception:
            self.save_failure_info(
                ref_table="govt_bld_area_infos",
                current_house_id=response.request.meta.get("house_id"),
                current_kapt_code=response.request.meta.get("kapt_code"),
                current_bld_name=response.request.meta.get("name"),
                new_dong_address=response.request.meta.get("new_dong_address"),
                origin_dong_address=response.request.meta.get("origin_dong_address"),
                bjd_code=response.request.meta.get("bjd_code"),
                current_url=response.request.meta.get("url"),
                bun=response.request.meta.get("bun"),
                ji=response.request.meta.get("ji"),
                response_or_failure=response,
            )

        try:
            item: GovtBldAreaInfoItem = GovtBldAreaInfoItem(
                house_id=response.request.meta["house_id"],
                mgm_bldrgst_pk=xml_to_dict.get("mgmBldrgstPk"),
                regstr_gb_cd=xml_to_dict.get("regstrGbCd"),
                regstr_gb_cd_nm=xml_to_dict.get("regstrGbCdNm"),
                regstr_kind_cd=xml_to_dict.get("regstrKindCd"),
                regstr_kind_cd_nm=xml_to_dict.get("regstrKindCdNm"),
                new_plat_plc=xml_to_dict.get("newPlatPlc"),
                bld_nm=xml_to_dict.get("bldNm"),
                splot_nm=xml_to_dict.get("splotNm"),
                block=xml_to_dict.get("block"),
                lot=xml_to_dict.get("lot"),
                bylot_cnt=xml_to_dict.get("bylotCnt"),
                na_road_cd=xml_to_dict.get("naRoadCd"),
                na_bjdong_cd=xml_to_dict.get("naBjdongCd"),
                na_ugrnd_cd=xml_to_dict.get("naUgrndCd"),
                na_main_bun=xml_to_dict.get("naMainBun"),
                na_sub_bun=xml_to_dict.get("naSubBun"),
                dong_nm=xml_to_dict.get("dongNm"),
                ho_nm=xml_to_dict.get("hoNm"),
                flr_gb_cd=xml_to_dict.get("flrGbCd"),
                flr_gb_cd_nm=xml_to_dict.get("flrGbCdNm"),
                flr_no=xml_to_dict.get("flrNo"),
                flr_no_nm=xml_to_dict.get("flrNoNm"),
                expos_pubuse_gb_cd=xml_to_dict.get("exposPubuseGbCd"),
                expos_pubuse_gb_cd_nm=xml_to_dict.get("exposPubuseGbCdNm"),
                main_atch_gb_cd=xml_to_dict.get("mainAtchGbCd"),
                main_atch_gb_cd_nm=xml_to_dict.get("mainAtchGbCdNm"),
                strct_cd=xml_to_dict.get("strctCd"),
                strct_cd_nm=xml_to_dict.get("strctCdNm"),
                etc_strct=xml_to_dict.get("etcStrct"),
                main_purps_cd=xml_to_dict.get("mainPurpsCd"),
                main_purps_cd_nm=xml_to_dict.get("mainPurpsCdNm"),
                etc_purps=xml_to_dict.get("etcPurps"),
                area=xml_to_dict.get("area"),
                crtn_day=xml_to_dict.get("crtnDay"),
                rnum=xml_to_dict.get("rnum"),
                plat_plc=xml_to_dict.get("platPlc"),
                sigungu_cd=xml_to_dict.get("sigunguCd"),
                bjdong_cd=xml_to_dict.get("bjdongCd"),
                plat_gb_cd=xml_to_dict.get("platGbCd"),
                bun=xml_to_dict.get("bun"),
                ji=xml_to_dict.get("ji"),
            )
        except KeyError:
            pass

        if item and item.mgm_bldrgst_pk:
            yield item
        else:
            self.save_failure_info(
                ref_table="govt_bld_area_infos",
                current_house_id=response.request.meta.get("house_id"),
                current_kapt_code=response.request.meta.get("kapt_code"),
                current_bld_name=response.request.meta.get("name"),
                new_dong_address=response.request.meta.get("new_dong_address"),
                origin_dong_address=response.request.meta.get("origin_dong_address"),
                bjd_code=response.request.meta.get("bjd_code"),
                current_url=response.request.meta.get("url"),
                bun=response.request.meta.get("bun"),
                ji=response.request.meta.get("ji"),
                response_or_failure=response,
            )

    def error_callback_bld_top_info(self, failure):
        self.save_failure_info(
            ref_table="govt_bld_top_infos",
            current_house_id=failure.request.meta.get("house_id"),
            current_kapt_code=failure.request.meta.get("kapt_code"),
            current_bld_name=failure.request.meta.get("name"),
            new_dong_address=failure.request.meta.get("new_dong_address"),
            origin_dong_address=failure.request.meta.get("origin_dong_address"),
            bjd_code=failure.request.meta.get("bjd_code"),
            current_url=failure.request.meta.get("url"),
            bun=failure.request.meta.get("bun"),
            ji=failure.request.meta.get("ji"),
            response_or_failure=failure,
        )

    def error_callback_bld_mid_info(self, failure):
        self.save_failure_info(
            ref_table="govt_bld_middle_infos",
            current_house_id=failure.request.meta.get("house_id"),
            current_kapt_code=failure.request.meta.get("kapt_code"),
            current_bld_name=failure.request.meta.get("name"),
            new_dong_address=failure.request.meta.get("new_dong_address"),
            origin_dong_address=failure.request.meta.get("origin_dong_address"),
            bjd_code=failure.request.meta.get("bjd_code"),
            current_url=failure.request.meta.get("url"),
            bun=failure.request.meta.get("bun"),
            ji=failure.request.meta.get("ji"),
            response_or_failure=failure,
        )

    def error_callback_bld_area_info(self, failure):
        self.save_failure_info(
            ref_table="govt_bld_area_infos",
            current_house_id=failure.request.meta.get("house_id"),
            current_kapt_code=failure.request.meta.get("kapt_code"),
            current_bld_name=failure.request.meta.get("name"),
            new_dong_address=failure.request.meta.get("new_dong_address"),
            origin_dong_address=failure.request.meta.get("origin_dong_address"),
            bjd_code=failure.request.meta.get("bjd_code"),
            current_url=failure.request.meta.get("url"),
            bun=failure.request.meta.get("bun"),
            ji=failure.request.meta.get("ji"),
            response_or_failure=failure,
        )

    def get_input_infos(
        self, bld_info_list: list[GovtBldInputEntity]
    ) -> list[GovtBldInputInfo] | None:
        input_infos: list[GovtBldInputInfo] | None = list()
        for elm in bld_info_list:
            extracted: GovtBldInputInfo | None = self._extract_input_params(
                bld_info=elm
            )
            if extracted:
                input_infos.append(self._extract_input_params(bld_info=elm))

        return input_infos

    def _extract_input_params(
        self, bld_info: GovtBldInputEntity
    ) -> GovtBldInputInfo | None:
        """'0000' : 공공데이터 번지 파라미터 default value format"""
        bunji_pattern = re.compile(r"[\d\-]")
        bun = "0000"
        ji = "0000"

        address: str | None = None
        # new_dong_address 가 있을 경우, 우선적으로 사용, 그렇지 않으면 origin_dong_address 사용
        if bld_info.new_dong_address:
            if bld_info.name in bld_info.new_dong_address:
                address = bld_info.new_dong_address.replace(" " + bld_info.name, "")
        else:
            if bld_info.name in bld_info.origin_dong_address:
                address = bld_info.origin_dong_address.replace(" " + bld_info.name, "")

        # pattern: 563-2
        # <주소 형태>
        # 1. 서울특별시 서초구 xx동 123-4 xx아파트 -> xx아파트 제거 후 지번 추출
        # 2. xx시 xx구 xx동 123-4 -> 바로 지번 추출
        # 3. xx시 xx구 xx동 xx아파트 -> 지번 초기값 사용
        if address and re.findall(bunji_pattern, address):
            bunji = address.split(" ")[-1]
        else:
            if bld_info.new_dong_address and re.fullmatch(
                bunji_pattern, bld_info.new_dong_address
            ):
                bunji = bld_info.new_dong_address.split(" ")[-1]
            elif bld_info.origin_dong_address and re.fullmatch(
                bunji_pattern, bld_info.origin_dong_address
            ):
                bunji = bld_info.origin_dong_address.split(" ")[-1]
            else:
                bunji = None

        if bunji:
            if "-" in bunji:
                bun = bun[len(bunji.split("-")[0]) :] + bunji.split("-")[0]
                ji = ji[len(bunji.split("-")[-1]) :] + bunji.split("-")[-1]
            else:
                bun = bun[len(bunji.split("-")[0]) :] + bunji.split("-")[0]

        if bld_info.bjd_code:
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
        else:
            return None

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
        bun,
        ji,
        response_or_failure,
    ) -> None:
        try:
            fail_orm: CallFailureHistoryModel = CallFailureHistoryModel(
                ref_id=current_house_id,
                ref_table=ref_table,
                param=f"url: {current_url}, "
                f"kapt_code: {current_kapt_code}, "
                f"current_bld_name: {current_bld_name}, "
                f"origin_dong_address: {origin_dong_address}, "
                f"new_dong_address: {new_dong_address}, "
                f"bun: {bun}, "
                f"ji: {ji}, "
                f"bjd_code: {bjd_code}",
                reason=f"response:{response_or_failure.text}",
            )
        except AttributeError:
            fail_orm: CallFailureHistoryModel = CallFailureHistoryModel(
                ref_id=current_house_id,
                ref_table=ref_table,
                param=f"url: {current_url}, "
                f"kapt_code: {current_kapt_code}, "
                f"current_bld_name: {current_bld_name}, "
                f"origin_dong_address: {origin_dong_address}, "
                f"new_dong_address: {new_dong_address}, "
                f"bjd_code: {bjd_code}",
                reason=f"response:{response_or_failure}",
            )
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

    def _change_service_key(self) -> bool:
        if GovtBldSpider.open_api_service_key == GovtBldEnum.SERVICE_KEY_1.value:
            GovtBldSpider.open_api_service_key = GovtBldEnum.SERVICE_KEY_2.value
            return True
        elif GovtBldSpider.open_api_service_key == GovtBldEnum.SERVICE_KEY_2.value:
            GovtBldSpider.open_api_service_key = GovtBldEnum.SERVICE_KEY_3.value
            return True
        elif GovtBldSpider.open_api_service_key == GovtBldEnum.SERVICE_KEY_3.value:
            GovtBldSpider.open_api_service_key = GovtBldEnum.SERVICE_KEY_4.value
            return True
        return False
