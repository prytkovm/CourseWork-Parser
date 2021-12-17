import scrapy
from ..items import ParseItem


class CitilinkSpider(scrapy.Spider):

    name = 'Citilink'
    allowed_domains = ['https://www.citilink.ru/catalog/noutbuki/']

    def __init__(self, category=None, *args, **kwargs):
        super(CitilinkSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.citilink.ru/catalog/{category}']
        # print(args)

    def parse(self, response):
        names = response.css(".ProductCardHorizontal__title::text").extract()
        prices = response.css(".ProductCardHorizontal__price_current-price::text").extract()
        for i in zip(names, prices):
            item = ParseItem()
            item['name'] = i[0]
            item['price'] = i[1].replace("\n", "").replace(" ", "")
            yield item

