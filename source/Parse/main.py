from Parse.spiders.Citilink import CitilinkSpider
from Parse.spiders.Eldorado import EldoradoSpider
from Parse.spiders.OnlineTrade import OnlineTradeSpider
from Parse.spiders.Ozon import OzonSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


# Init of UI and APP objects should be here...

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(CitilinkSpider, category="catalog/snegouborschiki/")
    process.start()
