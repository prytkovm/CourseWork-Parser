from parse.spiders.Citilink import CitilinkSpider
from parse.spiders.Eldorado import EldoradoSpider
from parse.spiders.OnlineTrade import OnlineTradeSpider
from parse.spiders.Ozon import OzonSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


# Init of UI and APP objects should be here...

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(OzonSpider, sub="category/umnye-chasy-i-fitnes-braslety-1761/")
    # process.crawl(OnlineTradeSpider, sub="catalogue/smartfony-c13/")
    # process.crawl(CitilinkSpider, sub="catalog/ekshn-kamery/asdasf")
    process.start()
