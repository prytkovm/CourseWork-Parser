import scrapy
from ..items import ParseItem


class OnlineTradeSpider(scrapy.Spider):
    name = 'OnlineTrade'
    allowed_domains = ['https://www.onlinetrade.ru/catalogue/']

    def __init__(self, category=None, *args, **kwargs):
        super(OnlineTradeSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.onlinetrade.ru/catalogue/{category}']

    def parse(self, response):
        names = response.css(".indexGoods__item__name::text").extract()
        prices = response.css(".price::text").extract()
        for i in zip(names, prices):
            item = ParseItem()
            item['name'] = i[0]
            item['price'] = i[1].replace("₽", "").replace(" ", "")
            yield item

