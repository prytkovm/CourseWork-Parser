import scrapy
from ..items import ProductItem


class EldoradoSpider(scrapy.Spider):

    def __init__(self, sub=None, parse_item_only=False, parse_goods=False):
        self.name = 'Eldorado'
        self.parse_item_only = parse_item_only
        self.parse_goods = parse_goods
        self.start_urls = [f'https://www.eldorado.ru/{sub}']
        super(EldoradoSpider, self).__init__()

    def parse(self, response):
        names = response.css(".sG::text").extract()
        temp_prices = response.css(".eS.lS::text").extract()
        prices = [item.strip() for item in temp_prices if item != '\xa0']
        for i in zip(names, prices):
            item = ProductItem()
            item['name'] = i[0]
            item['price'] = i[1].strip()
            yield item
        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def extract_product_data(self, product):
        pass

    def start_requests(self):
        for url in self.start_urls:
            if self.parse_item_only:
                yield scrapy.Request(
                    url=url,
                    callback=self.extract_product_data)
            elif self.parse_goods:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse)