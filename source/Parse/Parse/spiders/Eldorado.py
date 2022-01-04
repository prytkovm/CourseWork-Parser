import scrapy
from ..items import ParseItem


class EldoradoSpider(scrapy.Spider):

    def __init__(self, sub=None):
        self.name = 'Eldorado'
        self.start_urls = [f'https://www.eldorado.ru/{sub}']
        super(EldoradoSpider, self).__init__()

    def parse(self, response):
        names = response.css(".sG::text").extract()
        temp_prices = response.css(".eS.lS::text").extract()
        prices = [item.strip() for item in temp_prices if item != '\xa0']
        for i in zip(names, prices):
            item = ParseItem()
            item['name'] = i[0]
            item['price'] = i[1].replace(" ", "")
            yield item
        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
