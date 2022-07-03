import math

from scrapy import Spider, Request
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from modules.adapter.infrastructure.crawler.crawler.enum.subs_info_enum import SubscriptionInfoEnum


class SubscriptionSpider(Spider):
    name: str = "subscription_infos"
    custom_settings: dict = {
        # "ITEM_PIPELINES": {
        #     "modules.adapter.infrastructure.crawler.crawler.pipelines.LegalCodePipeline": 300
        # },
        "DOWNLOADER_MIDDLEWARES": {
            "modules.adapter.infrastructure.crawler.crawler.middlewares.SeleniumDownloaderMiddleware": 100
        }
    }
    start_ym: str = SubscriptionInfoEnum.START_YEAR_MONTH.value
    end_ym: str = SubscriptionInfoEnum.END_YEAR_MONTH.value
    last_page: int = 0

    def start_requests(self):
        url = SubscriptionInfoEnum.APPLY_HOME_URL.value
        yield Request(url=url)

    def browser_interaction_before_parsing(self, driver: WebDriver, request: Request):
        print("[SubscriptionSpider][browser_interaction_before_parsing] - get in!!!!!!!!!!!")

        self._set_date_select_box_event(
            start_date=SubscriptionSpider.start_ym,
            end_date=SubscriptionSpider.end_ym,
            driver=driver
        )

        SubscriptionSpider.last_page = self._find_last_page(driver=driver)

    def parse(self, response, **kwargs):
        print("parse!!!!!!!!!!")
        print(SubscriptionSpider.last_page)

    def _set_date_select_box_event(self, start_date: str, end_date: str, driver: WebDriver):
        select_start = Select(driver.find_element(By.CSS_SELECTOR, "#start_year"))
        select_start.select_by_visible_text(start_date)
        select_end = Select(driver.find_element(By.CSS_SELECTOR, "#end_year"))
        select_end.select_by_visible_text(end_date)
        driver.find_element(By.CSS_SELECTOR, ".search_btn").click()

    def _find_last_page(self, driver: WebDriver):
        total_txt_frame = driver.find_element(By.CLASS_NAME, "total_txt")
        total_txt_num = total_txt_frame.find_element(By.CLASS_NAME, "color_blue").text
        total_txt_num = int(total_txt_num)
        last_page = math.ceil(total_txt_num / 10)
        return last_page
