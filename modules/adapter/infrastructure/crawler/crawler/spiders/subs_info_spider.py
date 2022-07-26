import math
import re
import time

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from pandas import DataFrame
from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from modules.adapter.infrastructure.crawler.crawler.enum.subs_info_enum import (
    SubscriptionInfoEnum,
)
from modules.adapter.infrastructure.pypubsub.enum.subs_info_enum import (
    SubsInfoTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.event_listener import event_listener_dict
from modules.adapter.infrastructure.pypubsub.event_observer import send_message
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.subs_entity import (
    SubscriptionInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_info_model import (
    SubscriptionInfoModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SubscriptionSpider(Spider):
    name: str = "subscription_infos"
    custom_settings: dict = {
        "DOWNLOADER_MIDDLEWARES": {
            "modules.adapter.infrastructure.crawler.crawler.middlewares.SeleniumDownloaderMiddleware": 100
        }
    }
    start_ym: str = SubscriptionInfoEnum.START_YEAR_MONTH.value
    end_ym: str = SubscriptionInfoEnum.END_YEAR_MONTH.value
    scan_results: DataFrame | None = None
    subs_info_last_id_seq: int = 0

    def start_requests(self):
        SubscriptionSpider.subs_info_last_id_seq = self.subs_info_last_id_seq
        url = SubscriptionInfoEnum.APPLY_HOME_URL.value
        yield Request(url=url)

    def browser_interaction_before_parsing(self, driver: WebDriver):
        self._set_date_select_box_event(
            start_date=SubscriptionSpider.start_ym,
            end_date=SubscriptionSpider.end_ym,
            driver=driver,
        )

        self.scan_apply_home(
            driver=driver, last_page=self._get_last_page(driver=driver)
        )

    def scan_apply_home(self, driver: WebDriver, last_page: int):
        for page in range(1, last_page + 1):
            df_result_html: DataFrame = self._get_lookup_html(driver=driver, page=page)
            df_main_content: DataFrame = self._get_lookup_contents_per_each_row(
                driver=driver, page=page
            )
            df_detail: DataFrame = self._get_house_detail_data(driver=driver, page=page)
            df_competition: DataFrame = self._get_competition_data(
                driver=driver, page=page
            )

            merged_df = self._join_df(
                df_result_html, df_detail, df_main_content, df_competition
            )

            if page == 1:
                SubscriptionSpider.scan_results = merged_df.copy()
            else:
                SubscriptionSpider.scan_results = pd.concat(
                    [SubscriptionSpider.scan_results, merged_df], axis=0, join="outer"
                )

            try:
                self._click_next_page(
                    driver=driver, current_page=page, last_page=last_page
                )
                time.sleep(2.5)
            except Exception:
                time.sleep(1)
                self._click_next_page(
                    driver=driver, current_page=page, last_page=last_page
                )
                time.sleep(2.5)

        SubscriptionSpider.scan_results["발표날짜"] = pd.to_datetime(
            SubscriptionSpider.scan_results["당첨자발표 순으로 정렬"]
        )

        # 모집공고일 기준 일자별 필터링 필요한 경우 mask 사용
        # start = "{}-{}-{}".format(start_year, start_month, start_day)
        # end = "{}-{}-{}".format(end_year, end_month, end_day)
        # mask = (SubscriptionSpider.scan_results["모집공고일"] >= start) & (SubscriptionSpider.scan_results["모집공고일"] <= end)
        # SubscriptionSpider.scan_results = SubscriptionSpider.scan_results.loc[mask]

        if (
            SubscriptionSpider.scan_results is None
            or len(SubscriptionSpider.scan_results) == 0
        ):
            raise Exception("아무 데이터도 불러오지 못함")

        columns = {
            "당첨자발표 순으로 정렬": "발표일",
            "주택명 순으로 정렬": "주택명",
            "2순위 청약금": "청약금_2순위",
            "1·2순위 경쟁률": "경쟁률_1_2순위",
            "시공사": "건설업체",
        }
        SubscriptionSpider.scan_results.rename(columns=columns, inplace=True)

        SubscriptionSpider.scan_results = self._clean_up_columns(
            SubscriptionSpider.scan_results
        )

        # Unique값에 Null제거
        unique_keys = ["모집공고일", "발표일", "주택명", "주택형"]
        SubscriptionSpider.scan_results = self._remove_null_in_unique(
            SubscriptionSpider.scan_results, unique_keys
        )
        SubscriptionSpider.scan_results = SubscriptionSpider.scan_results.where(
            (pd.notnull(SubscriptionSpider.scan_results)), None
        )

        rename_columns = {
            "주택형": "area_type",
            "공급금액(최고가 기준)": "supply_price",
            "청약금_2순위": "second_subs_amount",
            "주소": "origin_address",
            "공급규모": "supply_household",
            "모집공고주소": "offer_notice_url",
            "입주예정월": "move_in_date",
            "계약일": "contract_date",
            "홈페이지주소": "hompage_url",
            "해당지역_특별공급_일정": "special_supply_date",
            "기타지역_특별공급_일정": "special_supply_etc_date",
            "기타경기_특별공급_일정": "special_etc_gyeonggi_date",
            "해당지역_1순위_일정": "first_supply_date",
            "기타지역_1순위_일정": "first_supply_etc_date",
            "기타경기_1순위_일정": "first_etc_gyeonggi_date",
            "해당지역_2순위_일정": "second_supply_date",
            "기타지역_2순위_일정": "second_supply_etc_date",
            "기타경기_2순위_일정": "second_etc_gyeonggi_date",
            "주택공급면적": "supply_area",
            "지역": "region",
            "주택구분": "housing_category",
            "분양/임대": "rent_type",
            "주택명": "name",
            "건설업체": "construct_company",
            "문의처": "contact",
            "청약기간 순으로 정렬": "subscription_date",
            "모집공고일": "offer_date",
            "발표일": "notice_winner_date",
            "특별공급신청현황": "special_supply_status",
            "경쟁률_1_2순위": "cmptt_rank",
            "다자녀_가구_기타경기": "multi_children_vol_etc_gyeonggi",
            "다자녀_가구_기타지역": "multi_children_vol_etc",
            "다자녀_가구_배정세대수": "multi_children_household",
            "다자녀_가구_해당지역": "multi_children_vol",
            "신혼_부부_기타경기": "newlywed_vol_etc_gyeonggi",
            "신혼_부부_기타지역": "newlywed_vol_etc",
            "신혼_부부_배정세대수": "newlywed_household",
            "신혼_부부_해당지역": "newlywed_vol",
            "생애최초_기타경기": "first_life_vol_etc_gyeonggi",
            "생애최초_기타지역": "first_life_vol_etc",
            "생애최초_배정세대수": "first_life_household",
            "생애최초_해당지역": "first_life_vol",
            "노부모_부양_기타경기": "old_parent_vol_etc_gyeonggi",
            "노부모_부양_기타지역": "old_parent_vol_etc",
            "노부모_부양_배정세대수": "old_parent_household",
            "노부모_부양_해당지역": "old_parent_vol",
            "기관_추천_기타경기": "agency_recommend_etc_gyeonggi",
            "기관_추천_기타지역": "agency_recommend_etc",
            "기관_추천_배정세대수": "agency_recommend_house_hold",
            "기관_추천_해당지역": "agency_recommend_vol",
            "일반공급_실질_공급세대수": "official_general_household",
            "일반공급_공급세대수": "general_household",
            "특별공급_공급세대수": "special_household",
            "1순위당해_접수건수": "first_accept_cnt",
            "1순위기타_접수건수": "first_accept_cnt_etc",
            "1순위경기_접수건수": "first_accept_cnt_gyeonggi",
            "2순위당해_접수건수": "second_accept_cnt",
            "2순위기타_접수건수": "second_accept_cnt_etc",
            "2순위경기_접수건수": "second_accept_cnt_gyeonggi",
            "1순위당해_순위내경쟁률": "first_cmptt_rate",
            "1순위경기_순위내경쟁률": "first_cmptt_rate_gyeonggi",
            "1순위기타_순위내경쟁률": "first_cmptt_rate_etc",
            "2순위당해_순위내경쟁률": "second_cmptt_rate",
            "2순위경기_순위내경쟁률": "second_cmptt_rate_gyeonggi",
            "2순위기타_순위내경쟁률": "second_cmptt_rate_etc",
            "기타지역_당첨가점최저": "lowest_win_point_etc",
            "해당지역_당첨가점최저": "lowest_win_point",
            "기타경기_당첨가점최저": "lowest_win_point_gyeonggi",
            "기타지역_당첨가점최고": "top_win_point_etc",
            "해당지역_당첨가점최고": "top_win_point",
            "기타경기_당첨가점최고": "top_win_point_gyeonggi",
            "기타지역_당첨가점평균": "avg_win_point_etc",
            "해당지역_당첨가점평균": "avg_win_point",
            "기타경기_당첨가점평균": "avg_win_point_gyeonggi",
            "subs_id": "subs_id",
        }
        SubscriptionSpider.scan_results.rename(columns=rename_columns, inplace=True)

        SubscriptionSpider.scan_results["name"] = SubscriptionSpider.scan_results[
            "name"
        ].str.replace("'", "")

    def parse(self, response, **kwargs):
        subs_info_dicts: list[dict] = self.convert_result_to_list()
        parsed_subs_info_models: list[SubscriptionInfoModel] = list()
        create_list: list[SubscriptionInfoModel] = list()
        update_list: list[SubscriptionInfoModel] = list()

        for subs_info_dict in subs_info_dicts:
            parsed_subs_info_models.append(SubscriptionInfoModel(**subs_info_dict))

        subs_infos_from_current_db: list[
            SubscriptionInfoEntity
        ] = self.__find_subs_infos_by_year_month()

        if subs_infos_from_current_db:
            for parsed_info in parsed_subs_info_models:
                for subs_info in subs_infos_from_current_db:
                    if (
                        parsed_info.name == subs_info.name
                        and parsed_info.offer_date == subs_info.offer_date
                        and parsed_info.rent_type == subs_info.rent_type
                        and parsed_info.area_type == subs_info.area_type
                        and str(int(parsed_info.supply_price)) == subs_info.supply_price
                    ):
                        parsed_info.id = subs_info.id
                        update_list.append(parsed_info)

            if update_list:
                for parsed_info in parsed_subs_info_models:
                    if parsed_info not in update_list:
                        create_list.append(parsed_info)
            else:
                for parsed_info in parsed_subs_info_models:
                    create_list.append(parsed_info)
        else:
            for parsed_info in parsed_subs_info_models:
                create_list.append(parsed_info)

        if create_list:
            self._save_subs_infos(subs_infos=create_list)

        if update_list:
            for elm in update_list:
                self._update(elm)

        self.repo.update_id_to_code_rules(
            key_div="subs_id", last_id=SubscriptionSpider.subs_info_last_id_seq
        )

    def convert_result_to_list(self) -> list[dict]:
        result_to_list: list = list()
        for idx, row in SubscriptionSpider.scan_results.iterrows():
            temp_dic = row.to_dict()
            temp_dic = {
                key: None if self._is_nan(val) else val for key, val in temp_dic.items()
            }
            result_to_list.append(temp_dic)

        return result_to_list

    def _set_date_select_box_event(
        self, start_date: str, end_date: str, driver: WebDriver
    ) -> None:
        select_start = Select(driver.find_element(By.CSS_SELECTOR, "#start_year"))
        select_start.select_by_visible_text(start_date)
        select_end = Select(driver.find_element(By.CSS_SELECTOR, "#end_year"))
        select_end.select_by_visible_text(end_date)
        driver.find_element(By.CSS_SELECTOR, ".search_btn").click()

    def _get_last_page(self, driver: WebDriver) -> int:
        total_txt_frame = driver.find_element(By.CLASS_NAME, "total_txt")
        total_txt_num = total_txt_frame.find_element(By.CLASS_NAME, "color_blue").text
        total_txt_num = int(total_txt_num)
        last_page = math.ceil(total_txt_num / 10)

        return last_page

    def _get_lookup_html(self, driver: WebDriver, page: int) -> DataFrame:
        inner_html: str = driver.page_source
        bs: BeautifulSoup = BeautifulSoup(inner_html, "html.parser")
        tags = bs.find("table", attrs={"class": "tbl_st"})

        df: DataFrame = pd.read_html(str(tags), header=0)[0]

        df = df.reset_index()
        df["index"] = df["index"] + (page - 1) * 10
        return df

    def _set_apt_type(self, data) -> str:
        if type(data) is float or type(data) is int or type(data) is np.float64:
            if data < 100:
                if data < 10:
                    result = "".join(["00", str(data)])
                else:
                    result = "".join(["0", str(data)])
            else:
                result = str(data)

            if len(result) == 7:
                return "".join([result, "0"])
            elif len(result) == 6:
                return "".join([result, "00"])
            elif len(result) == 5:
                return "".join([result, "000"])
            else:
                return result

        else:
            return str(data)

    def _get_data_innerhtml(self, driver: WebDriver) -> DataFrame:
        time.sleep(0.2)
        driver.switch_to.frame("iframeDialog")
        inner_html = driver.page_source
        bs: BeautifulSoup = BeautifulSoup(inner_html, "html.parser")
        try:
            tags = bs.find_all("table", attrs={"class": "tbl_st"})[0]
        except Exception:
            time.sleep(30)
            tags = bs.find_all("table", attrs={"class": "tbl_st"})[0]

        table: DataFrame = pd.read_html(str(tags))[0]

        driver.switch_to.parent_frame()
        return table

    def _get_lookup_contents_per_each_row(
        self, driver: WebDriver, page: int
    ) -> DataFrame | None:
        table = driver.find_element(By.CLASS_NAME, "tbl_st")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        df_apply = pd.DataFrame()
        for i in range(len(rows)):
            try:
                body = rows[i].find_elements(By.TAG_NAME, "td")
            except Exception:
                time.sleep(1)
                driver.find_element(By.CLASS_NAME, "ui-button").click()
                body = rows[i].find_elements(By.TAG_NAME, "td")

            button_apply_stat = body[9].find_elements(By.TAG_NAME, "button")
            if len(button_apply_stat) > 0:
                button_apply_stat[0].click()
                time.sleep(2.5)
                try:
                    df_temp = self._get_data_innerhtml(driver=driver)
                except Exception:
                    time.sleep(2)
                    try:
                        button_apply_stat[0].click()
                        df_temp = self._get_data_innerhtml(driver=driver)
                    except Exception:
                        time.sleep(2)
                        df_temp = self._get_data_innerhtml(driver=driver)

                df_temp["index"] = int(i) + (page - 1) * 10

                if len(df_apply) == 0:
                    df_apply = df_temp.copy()
                else:
                    df_apply = pd.concat([df_apply, df_temp])

                driver.find_element(By.CLASS_NAME, "ui-button").click()

        if len(df_apply) == 0:
            return None

        df_apply = df_apply.sort_values("index")
        df_apply.columns = df_apply.columns.droplevel()

        columns = {
            "공급 세대수": "특별공급_공급세대수",
            "다자녀 가구": "다자녀_가구",
            "신혼 부부": "신혼_부부",
            "노부모 부양": "노부모_부양",
            "기관 추천": "기관_추천",
            "": "index",
        }

        df_apply = df_apply.rename(columns=columns)

        df_apply = pd.pivot(
            df_apply,
            columns="지역",
            values=["다자녀_가구", "신혼_부부", "생애최초", "노부모_부양", "기관_추천"],
            index=["index", "주택형", "특별공급_공급세대수"],
        )

        columns_level0 = list(df_apply.columns.droplevel(0))
        columns_level1 = list(df_apply.columns.droplevel(1))
        columns = [
            str(x) + "_" + str(y) for x, y in zip(columns_level1, columns_level0)
        ]
        df_apply.columns = columns
        df_apply = df_apply.reset_index()
        df_apply["주택형"] = df_apply["주택형"].apply(self._set_apt_type)

        return df_apply

    def _get_innerhtml_detail_data(self, driver: WebDriver) -> DataFrame:
        time.sleep(0.2)
        driver.switch_to.frame("iframeDialog")
        inner_html = driver.page_source
        bs: BeautifulSoup = BeautifulSoup(inner_html, "html.parser")

        table_detail_data = bs.find_all("table", attrs={"class": "tbl_st"})[0]
        address = table_detail_data.find_all("td", attrs={"class": "txt_l"})[0].text
        apt_num = table_detail_data.find_all("td", attrs={"class": "txt_l"})[1].text
        table_name_ls = bs.find_all("h5")

        # 공급금액
        num = 0
        for i in range(len(table_name_ls)):
            if "공급금액" in table_name_ls[i].text:
                num = i

        tags = bs.find_all("table", attrs={"class": "tbl_st"})[num]
        table = pd.read_html(str(tags))[0]
        table["주소"] = address
        table["공급규모"] = apt_num

        # 모집공고 주소
        try:
            url = bs.find_all("a", attrs={"class": "radius_btn"})[0]
            url = url.get_attribute_list("href")[0]
            apply_home_url = "https://www.applyhome.co.kr"
            url = "".join([apply_home_url, url])
            table["모집공고주소"] = url
        except Exception:
            table["모집공고주소"] = None

        # 입주예정월
        tags = bs.find_all("ul", attrs={"class": "inde_txt"})
        num = 0
        for i in range(len(tags)):
            if "입주예정월" in tags[i].text:
                num = i

        text = tags[num].text
        match = re.search(r"\d{4}.\d{2}", text)
        table["입주예정월"] = match.group()

        # 청약일정
        num = 0
        for i in range(len(table_name_ls)):
            if "청약일정" in table_name_ls[i].text:
                num = i

        tags = bs.find_all("table", attrs={"class": "tbl_st"})[num]
        table_date = pd.read_html(str(tags), header=1)[0]
        table["계약일"] = table_date[table_date["청약접수"] == "계약일"]["구분"].iloc[0]
        homepage_addr_str = table_date[table_date["청약접수"] == "당첨자 발표일"]["구분"].iloc[0]
        try:
            table["홈페이지주소"] = re.findall("\(([^)]+)", homepage_addr_str)[0].strip()
        except Exception:
            table["홈페이지주소"] = None
        table_date = table_date.loc[:2]

        try:
            table_date["기타경기"]
        except KeyError:
            table_date["기타경기"] = None
        table_date = table_date[["구분", "해당지역", "기타지역", "기타경기"]]

        try:
            idx = table_date[table_date["구분"] == "특별공급"].index[0]
            value = table_date.iloc[idx]["해당지역"]
            table["해당지역_특별공급_일정"] = value
        except IndexError:
            table["해당지역_특별공급_일정"] = None

        try:
            idx = table_date[table_date["구분"] == "특별공급"].index[0]
            value = table_date.iloc[idx]["기타지역"]
            table["기타지역_특별공급_일정"] = value
        except IndexError:
            table["기타지역_특별공급_일정"] = None

        try:
            idx = table_date[table_date["구분"] == "특별공급"].index[0]
            value = table_date.iloc[idx]["기타경기"]
            table["기타경기_특별공급_일정"] = value
        except IndexError:
            table["기타경기_특별공급_일정"] = None

        idx = table_date[table_date["구분"] == "1순위"].index[0]
        value = table_date.iloc[idx]["해당지역"]
        table["해당지역_1순위_일정"] = value

        idx = table_date[table_date["구분"] == "1순위"].index[0]
        value = table_date.iloc[idx]["기타지역"]
        table["기타지역_1순위_일정"] = value

        idx = table_date[table_date["구분"] == "1순위"].index[0]
        value = table_date.iloc[idx]["기타경기"]
        table["기타경기_1순위_일정"] = value

        idx = table_date[table_date["구분"] == "2순위"].index[0]
        value = table_date.iloc[idx]["해당지역"]
        table["해당지역_2순위_일정"] = value

        idx = table_date[table_date["구분"] == "2순위"].index[0]
        value = table_date.iloc[idx]["기타지역"]
        table["기타지역_2순위_일정"] = value

        idx = table_date[table_date["구분"] == "2순위"].index[0]
        value = table_date.iloc[idx]["기타경기"]
        table["기타경기_2순위_일정"] = value

        # 공급대상
        num = 0
        for i in range(len(table_name_ls)):
            if "공급대상" in table_name_ls[i].text:
                num = i
                break

        tags = bs.find_all("table", attrs={"class": "tbl_st"})[num]
        table_range = pd.read_html(str(tags), header=1)[0]
        table_range = table_range[["주택형", "주택공급면적(주거전용+주거공용)", "일반"]].copy()
        columns = {"주택공급면적(주거전용+주거공용)": "주택공급면적", "일반": "일반공급_공급세대수"}
        table_range.rename(columns=columns, inplace=True)
        table_range = table_range.loc[: len(table_range) - 2]

        table["주택형"] = table["주택형"].apply(self._set_apt_type)

        table = pd.merge(table, table_range, how="left", on="주택형")

        driver.switch_to.parent_frame()

        return table

    def _get_house_detail_data(self, driver: WebDriver, page: int):
        """
        지역, 분양 가격 정보 불러옴

        :param page: 청약홈 분양 데이터 게시글 페이지
        :return: DataFrame
        """
        table = driver.find_element(By.CLASS_NAME, "tbl_st")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        df = pd.DataFrame()
        for i in range(len(rows)):
            try:
                body = rows[i].find_elements(By.TAG_NAME, "td")
                SubscriptionSpider.subs_info_last_id_seq = (
                    SubscriptionSpider.subs_info_last_id_seq + 1
                )
            except Exception:
                time.sleep(1)
                try:
                    driver.find_element(By.CLASS_NAME, "ui-button").click()
                except Exception:
                    driver.switch_to.parent_frame()
                    driver.find_element(By.CLASS_NAME, "ui-button").click()

                body = rows[i].find_elements(By.TAG_NAME, "td")

            button_detail_stat = body[3].find_elements(By.TAG_NAME, "a")[0]
            button_detail_stat.click()
            time.sleep(2.5)

            try:
                df_temp = self._get_innerhtml_detail_data(driver=driver)
            except Exception:
                try:
                    time.sleep(1)
                    button_detail_stat.click()
                    df_temp = self._get_innerhtml_detail_data(driver=driver)
                except Exception:
                    driver.switch_to.parent_frame()
                    driver.find_element(By.CLASS_NAME, "ui-button").click()
                    continue

            driver.find_element(By.CLASS_NAME, "ui-button").click()
            df_temp["index"] = int(i) + (page - 1) * 10
            df_temp["subs_id"] = SubscriptionSpider.subs_info_last_id_seq
            if len(df) == 0:
                df = df_temp.copy()
            else:
                df = pd.concat([df, df_temp])

        if len(df) == 0:
            return None
        else:
            df.reset_index(drop=True, inplace=True)
            return df

    def _get_innerhtml_competition_data(self, driver: WebDriver) -> DataFrame | None:
        try:
            time.sleep(0.2)
            driver.switch_to.frame("iframeDialog")
            inner_html = driver.page_source
            bs: BeautifulSoup = BeautifulSoup(inner_html, "html.parser")

            tags = bs.find_all("table", attrs={"class": "tbl_st"})[0]
            table = pd.read_html(str(tags))[0]
            columns = [
                "주택형",
                "일반공급_실질_공급세대수",
                "순위",
                "지역",
                "접수건수",
                "순위내경쟁률",
                "청약결과",
                "당첨가점_지역",
                "당첨가점_최저",
                "당첨가점_최고",
                "당첨가점_평균",
            ]
            table.columns = columns
        except Exception:
            driver.switch_to.parent_frame()
            return None

        table["주택형"] = table["주택형"].apply(self._set_apt_type)
        driver.switch_to.parent_frame()

        return table

    def _get_competition_data(self, driver: WebDriver, page: int) -> DataFrame | None:
        """
        청약홈 일반분양 경쟁률 데이터 크롤링함
        :return: DataFrame
        """

        table = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "tbl_st"))
        )
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        df = pd.DataFrame()
        for i in range(len(rows)):
            try:
                body = rows[i].find_elements(By.TAG_NAME, "td")
            except Exception:
                time.sleep(1)
                driver.find_element(By.CLASS_NAME, "ui-button").click()
                body = rows[i].find_elements(By.TAG_NAME, "td")

            button_detail_stat = body[10]
            if button_detail_stat.text == "사업주체문의":
                continue

            button_detail_stat.click()
            time.sleep(2.5)
            try:
                df_temp = self._get_innerhtml_competition_data(driver=driver)
            except Exception:
                time.sleep(1)
                button_detail_stat.click()
                df_temp = self._get_innerhtml_competition_data(driver=driver)

            try:
                driver.find_element(By.CLASS_NAME, "ui-button").click()
            except Exception:
                button_detail_stat.click()
                time.sleep(2.5)
                df_temp = self._get_innerhtml_competition_data(driver=driver)
                driver.find_element(By.CLASS_NAME, "ui-button").click()

            if df_temp is None:
                continue
            else:
                df_temp["index"] = int(i) + (page - 1) * 10

            if len(df) == 0:
                df = df_temp.copy()
            else:
                df = pd.concat([df, df_temp])

        df.reset_index(drop=True, inplace=True)
        if len(df) == 0:
            return None

        pivot_df1 = pd.pivot(
            df,
            columns=["순위", "지역"],
            values=["접수건수", "순위내경쟁률"],
            index=["주택형", "index", "일반공급_실질_공급세대수"],
        )

        try:
            drop_col = [("접수건수", "순위", np.nan), ("순위내경쟁률", "순위", np.nan)]
            pivot_df1.drop(columns=drop_col, inplace=True)
        except Exception:
            pass

        if len(pivot_df1.columns) == 8:
            pivot_df1.columns = ["_".join(str(col)) for col in pivot_df1.columns.values]
            pivot_df1.rename(
                columns={
                    "접수건수_1순위_해당지역": "1순위당해_접수건수",
                    "접수건수_1순위_기타지역": "1순위기타_접수건수",
                    "접수건수_2순위_해당지역": "2순위당해_접수건수",
                    "접수건수_2순위_기타지역": "2순위기타_접수건수",
                    "순위내경쟁률_1순위_해당지역": "1순위당해_순위내경쟁률",
                    "순위내경쟁률_1순위_기타지역": "1순위기타_순위내경쟁률",
                    "순위내경쟁률_2순위_해당지역": "2순위당해_순위내경쟁률",
                    "순위내경쟁률_2순위_기타지역": "2순위기타_순위내경쟁률",
                },
                inplace=True,
            )
            pivot_df1["1순위경기_접수건수"] = None
            pivot_df1["2순위경기_접수건수"] = None
            pivot_df1["1순위경기_순위내경쟁률"] = None
            pivot_df1["2순위경기_순위내경쟁률"] = None

        else:
            pivot_df1.columns = ["_".join(str(col)) for col in pivot_df1.columns.values]
            pivot_df1.rename(
                columns={
                    "접수건수_1순위_해당지역": "1순위당해_접수건수",
                    "접수건수_1순위_기타지역": "1순위기타_접수건수",
                    "접수건수_2순위_해당지역": "2순위당해_접수건수",
                    "접수건수_2순위_기타지역": "2순위기타_접수건수",
                    "접수건수_1순위_기타경기": "1순위경기_접수건수",
                    "접수건수_2순위_기타경기": "2순위경기_접수건수",
                    "순위내경쟁률_1순위_해당지역": "1순위당해_순위내경쟁률",
                    "순위내경쟁률_1순위_기타지역": "1순위기타_순위내경쟁률",
                    "순위내경쟁률_2순위_해당지역": "2순위당해_순위내경쟁률",
                    "순위내경쟁률_2순위_기타지역": "2순위기타_순위내경쟁률",
                    "순위내경쟁률_1순위_기타경기": "1순위경기_순위내경쟁률",
                    "순위내경쟁률_2순위_기타경기": "2순위경기_순위내경쟁률",
                },
                inplace=True,
            )

        df_point = df[
            [
                "주택형",
                "index",
                "일반공급_실질_공급세대수",
                "당첨가점_지역",
                "당첨가점_최저",
                "당첨가점_최고",
                "당첨가점_평균",
            ]
        ]
        df_point = df_point[df_point["당첨가점_지역"].isin(["해당지역", "기타경기", "기타지역"])]
        df_point = df_point.groupby(["주택형", "index", "당첨가점_지역"]).first()
        df_point.reset_index(drop=False, inplace=True)

        pivot_df2 = pd.pivot(
            df_point,
            columns="당첨가점_지역",
            values=["당첨가점_최저", "당첨가점_최고", "당첨가점_평균"],
            index=["주택형", "index", "일반공급_실질_공급세대수"],
        )

        if len(pivot_df2.columns) == 6:
            pivot_df2.columns = ["_".join(col) for col in pivot_df2.columns.values]
            pivot_df2.rename(
                columns={
                    "당첨가점_최저_기타지역": "기타지역_당첨가점최저",
                    "당첨가점_최저_해당지역": "해당지역_당첨가점최저",
                    "당첨가점_최고_기타지역": "기타지역_당첨가점최고",
                    "당첨가점_최고_해당지역": "해당지역_당첨가점최고",
                    "당첨가점_평균_기타지역": "기타지역_당첨가점평균",
                    "당첨가점_평균_해당지역": "해당지역_당첨가점평균",
                },
                inplace=True,
            )
            pivot_df2["기타경기_당첨가점최저"] = None
            pivot_df2["기타경기_당첨가점최고"] = None
            pivot_df2["기타경기_당첨가점평균"] = None

        elif len(pivot_df2.columns) == 9:
            pivot_df2.columns = ["_".join(col) for col in pivot_df2.columns.values]
            pivot_df2.rename(
                columns={
                    "당첨가점_최저_기타지역": "기타지역_당첨가점최저",
                    "당첨가점_최저_해당지역": "해당지역_당첨가점최저",
                    "당첨가점_최고_기타지역": "기타지역_당첨가점최고",
                    "당첨가점_최고_해당지역": "해당지역_당첨가점최고",
                    "당첨가점_평균_기타지역": "기타지역_당첨가점평균",
                    "당첨가점_평균_해당지역": "해당지역_당첨가점평균",
                    "당첨가점_최저_기타경기": "기타경기_당첨가점최저",
                    "당첨가점_최고_기타경기": "기타경기_당첨가점최고",
                    "당첨가점_평균_기타경기": "기타경기_당첨가점평균",
                },
                inplace=True,
            )

        elif len(pivot_df2.columns) == 3:
            pivot_df2.columns = ["해당지역_당첨가점최저", "해당지역_당첨가점최고", "해당지역_당첨가점평균"]

            pivot_df2.columns = ["_".join(str(col)) for col in pivot_df2.columns.values]
            pivot_df2.rename(
                columns={
                    "당첨가점_최저_해당지역": "해당지역_당첨가점최저",
                    "당첨가점_최고_해당지역": "해당지역_당첨가점최고",
                    "당첨가점_평균_해당지역": "해당지역_당첨가점평균",
                },
                inplace=True,
            )

            pivot_df2["기타지역_당첨가점최저"] = None
            pivot_df2["기타지역_당첨가점최고"] = None
            pivot_df2["기타지역_당첨가점평균"] = None

            pivot_df2["기타경기_당첨가점최저"] = None
            pivot_df2["기타경기_당첨가점최고"] = None
            pivot_df2["기타경기_당첨가점평균"] = None

        elif len(pivot_df2.columns) == 0:
            pivot_df2 = None
        else:
            raise Exception("competition error")

        if pivot_df2 is None:
            df_result = pivot_df1.copy()
            df_result.reset_index(inplace=True)
        else:
            df_result = pd.merge(
                pivot_df1, pivot_df2, how="outer", left_index=True, right_index=True
            )
            df_result.reset_index(inplace=True)

        if len(df_result) == 0:
            return None
        else:
            return df_result

    def _join_df(
        self,
        df_data: DataFrame,
        df_detail: DataFrame,
        df_apply: DataFrame,
        df_competition: DataFrame,
    ) -> DataFrame:
        if df_detail is None:
            merged_df = df_data.copy()
        else:
            merged_df = pd.merge(
                df_detail, df_data, how="outer", left_on="index", right_on="index"
            )

        if df_apply is None:
            pass
        else:
            try:
                merged_df = pd.merge(
                    merged_df, df_apply, how="outer", on=["index", "주택형"]
                )
            except Exception:
                if df_detail is None:
                    merged_df = pd.merge(merged_df, df_apply, how="outer", on=["index"])
                else:
                    pass

        if df_competition is None:
            pass
        else:
            try:
                merged_df = pd.merge(
                    merged_df, df_competition, how="outer", on=["index", "주택형"]
                )
            except Exception:
                pass

        return merged_df

    def _is_nan(self, data) -> bool:
        try:
            return np.isnan(data)
        except Exception:
            return False

    def _click_next_page(self, driver: WebDriver, current_page: int, last_page: int):
        next_page = current_page + 1
        if int(current_page) == int(last_page):
            return
        script = "fn_link_page(" + str(next_page) + ");return false;"
        driver.execute_script(script)

    def _remove_null_in_unique(self, df: DataFrame, unique_columns) -> DataFrame:
        for col in unique_columns:
            df = df[df[col].notnull()]
        return df

    def _clean_up_columns(self, df: DataFrame) -> DataFrame:
        result_columns = [
            "주택형",
            "공급금액(최고가 기준)",
            "청약금_2순위",
            "주소",
            "공급규모",
            "모집공고주소",
            "입주예정월",
            "계약일",
            "홈페이지주소",
            "해당지역_특별공급_일정",
            "기타지역_특별공급_일정",
            "기타경기_특별공급_일정",
            "해당지역_1순위_일정",
            "기타지역_1순위_일정",
            "기타경기_1순위_일정",
            "해당지역_2순위_일정",
            "기타지역_2순위_일정",
            "기타경기_2순위_일정",
            "주택공급면적",
            "지역",
            "주택구분",
            "분양/임대",
            "주택명",
            "건설업체",
            "문의처",
            "모집공고일",
            "청약기간 순으로 정렬",
            "발표일",
            "특별공급신청현황",
            "경쟁률_1_2순위",
            "다자녀_가구_기타경기",
            "다자녀_가구_기타지역",
            "다자녀_가구_배정세대수",
            "다자녀_가구_해당지역",
            "신혼_부부_기타경기",
            "신혼_부부_기타지역",
            "신혼_부부_배정세대수",
            "신혼_부부_해당지역",
            "생애최초_기타경기",
            "생애최초_기타지역",
            "생애최초_배정세대수",
            "생애최초_해당지역",
            "노부모_부양_기타경기",
            "노부모_부양_기타지역",
            "노부모_부양_배정세대수",
            "노부모_부양_해당지역",
            "기관_추천_기타경기",
            "기관_추천_기타지역",
            "기관_추천_배정세대수",
            "기관_추천_해당지역",
            "일반공급_실질_공급세대수",
            "일반공급_공급세대수",
            "특별공급_공급세대수",
            "1순위당해_접수건수",
            "1순위기타_접수건수",
            "1순위경기_접수건수",
            "2순위당해_접수건수",
            "2순위기타_접수건수",
            "2순위경기_접수건수",
            "1순위당해_순위내경쟁률",
            "1순위기타_순위내경쟁률",
            "1순위경기_순위내경쟁률",
            "2순위당해_순위내경쟁률",
            "2순위기타_순위내경쟁률",
            "2순위경기_순위내경쟁률",
            "기타지역_당첨가점최저",
            "해당지역_당첨가점최저",
            "기타경기_당첨가점최저",
            "기타지역_당첨가점최고",
            "해당지역_당첨가점최고",
            "기타경기_당첨가점최고",
            "기타지역_당첨가점평균",
            "해당지역_당첨가점평균",
            "기타경기_당첨가점평균",
            "subs_id",
        ]
        for item in result_columns:
            if item not in df.columns:
                df[item] = None
        df = df[result_columns]
        return df

    def _save_subs_infos(self, subs_infos: list[SubscriptionInfoModel]):
        if subs_infos:
            self.__save_all(subs_infos=subs_infos)

    def _update(self, subs_info: SubscriptionInfoModel):
        if subs_info:
            self.__update_subs_info(subs_info=subs_info)

    def _trans_date_format(self, year_month: str):
        return year_month.replace("년 ", "-").replace("월", "")

    def __save_all(self, subs_infos: list[SubscriptionInfoModel]) -> None:
        send_message(
            topic_name=SubsInfoTopicEnum.SAVE_ALL.value,
            values=subs_infos,
        )
        return event_listener_dict.get(f"{SubsInfoTopicEnum.SAVE_ALL.value}")

    def __update_subs_info(self, subs_info: SubscriptionInfoModel) -> None:
        send_message(
            topic_name=SubsInfoTopicEnum.UPDATE_TO_NEW_SCHEMA.value,
            subs_info=subs_info,
        )
        return event_listener_dict.get(
            f"{SubsInfoTopicEnum.UPDATE_TO_NEW_SCHEMA.value}"
        )

    def __find_subs_infos_by_year_month(self) -> list[SubscriptionInfoEntity]:
        start_year_month = self._trans_date_format(
            year_month=SubscriptionSpider.start_ym
        )
        end_year_month = self._trans_date_format(year_month=SubscriptionSpider.end_ym)

        send_message(
            topic_name=SubsInfoTopicEnum.FIND_SUBSCRIPTION_INFOS_BY_YEAR_MONTH.value,
            start_year_month=start_year_month,
            end_year_month=end_year_month,
        )
        return event_listener_dict.get(
            f"{SubsInfoTopicEnum.FIND_SUBSCRIPTION_INFOS_BY_YEAR_MONTH.value}"
        )
