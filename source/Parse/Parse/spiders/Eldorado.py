import scrapy
from ..items import ParseItem


class EldoradoSpider(scrapy.Spider):
    name = 'Eldorado'
    allowed_domains = ['https://www.eldorado.ru/d/']

    def __init__(self, category=None, *args, **kwargs):
        super(EldoradoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.eldorado.ru/d/{category}']

    def parse(self, response):
        names = response.css(".sG::text").extract()
        temp_prices = response.css(".eS.lS::text").extract()
        prices = [item.strip() for item in temp_prices if item != '\xa0']
        for i in zip(names, prices):
            item = ParseItem()
            item['name'] = i[0]
            item['price'] = i[1].replace(" ", "")
            yield item

