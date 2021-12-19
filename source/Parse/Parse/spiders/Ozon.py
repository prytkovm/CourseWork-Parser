import scrapy
from ..items import ParseItem


class OzonSpider(scrapy.Spider):

    def __init__(self, category=None, *args, **kwargs):
        self.name = 'Ozon'
        self.custom_settings = {'HTTPCACHE_ENABLED': False}
        self.start_urls = [f'https://www.ozon.ru/{category}']
        super(OzonSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        names = response.css(".a7y.a8a2.a8a6.a8b2.f-tsBodyL.bj5").extract()
        prices = response.css(".ui-p9.ui-q1.ui-q4::text").extract()
        for i in zip(names, prices):
            item = ParseItem()
            item['name'] = i[0].replace("<span class=\"a7y a8a2 a8a6 a8b2 f-tsBodyL bj5\" style=\"color:;\"><span>", "").replace("</span></span>", "")
            item['price'] = i[1].replace("\u2009", "").replace("₽", "")
            yield item
        next_page_url = response.css(".ui-b2::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))