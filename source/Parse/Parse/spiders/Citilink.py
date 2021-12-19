import scrapy
from ..items import ParseItem


class CitilinkSpider(scrapy.Spider):

    def __init__(self, category=None, *args, **kwargs):
        self.name = 'Citilink'
        self.start_urls = [f'https://www.citilink.ru/{category}']
        super(CitilinkSpider, self).__init__(*args, **kwargs)
        self.current_page = 1

    def parse(self, response):
        names = response.css(".ProductCardHorizontal__title::text").extract()
        prices = response.css(".ProductCardHorizontal__price_current-price::text").extract()
        for i in zip(names, prices):
            item = ParseItem()
            item['name'] = i[0]
            item['price'] = i[1].replace("\n", "").replace(" ", "")
            yield item
        self.current_page += 1
        #temp = f"a[data-page=\'{self.current_page}\']::attr(href)"
        #print(temp)
        next_page_url = response.css(f"a[data-page=\'{self.current_page}\']::attr(href)").get()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
