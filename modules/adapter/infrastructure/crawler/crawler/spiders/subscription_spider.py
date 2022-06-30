from scrapy import Spider, Request


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
        print("[SubscriptionSpider][start_requests]")
        url = "https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancListView.do"
        yield Request(url=url)

    def parse(self, response, **kwargs):
        print("parse!!!!!!!!!!")
        print(response)

