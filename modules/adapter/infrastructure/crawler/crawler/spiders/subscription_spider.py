from scrapy import Spider, Request
from selenium.webdriver.chrome.webdriver import WebDriver


class SubscriptionSpider(Spider):
    name = "subscription_infos"
    custom_settings = {
        # "ITEM_PIPELINES": {
        #     "modules.adapter.infrastructure.crawler.crawler.pipelines.LegalCodePipeline": 300
        # },
        "DOWNLOADER_MIDDLEWARES": {
            "modules.adapter.infrastructure.crawler.crawler.middlewares.SeleniumDownloaderMiddleware": 100
        }
    }

    def start_requests(self):
        url = "https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancListView.do"
        yield Request(url=url)

    def browser_interaction_before_parsing(self, driver: WebDriver, request: Request):
        print("[SubscriptionSpider][browser_interaction_before_parsing] - get in!!!!!!!!!!!")

    def parse(self, response, **kwargs):
        print("parse!!!!!!!!!!")
        print(response)


