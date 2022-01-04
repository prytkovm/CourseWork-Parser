import scrapy
from ..items import ParseItem


class OzonSpider(scrapy.Spider):

    def __init__(self, sub=None):
        self.name = 'Ozon'
        self.start_urls = [f'https://www.ozon.ru/{sub}']
        super(OzonSpider, self).__init__()
        self.current_page = 1
        # Пока так, чтобы не получать капчу, потом подрубим прокси
        self.max_pages = 40

    def parse(self, response):
        """ Перегрузка метода родительского класса """
        names = response.css("div[class*=\"bi3 bi5\"] >"
                             "div[class*=\"bi7\"] >"
                             "div[class*=\"bj\"] >"
                             "a > span > span::text").extract()
        prices = response.css("div[class*=\"bi3 bi5\"] >"
                              "div[class*=\"bi8\"] >"
                              "div[class*=\"ui-p6\"] > span::text").extract()

        for i in zip(names, prices):
            item = ParseItem()
            item['name'] = i[0]
            item['price'] = i[1].encode('utf-8').rstrip()
            yield item
        next_page_url = response.css("div > a[class*=\"ui-b2\"]::attr(href)").extract()
        self.current_page += 1
        if next_page_url is not None and self.current_page != self.max_pages:
            yield scrapy.Request(response.urljoin(next_page_url[-1]))
