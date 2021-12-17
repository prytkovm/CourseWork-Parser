import scrapy
from ..items import ParseItem

# Need to do smth with redirect(302, 307)


class DnsSpider(scrapy.Spider):
    name = 'DNS'
    allowed_domains = ['https://www.dns-shop.ru/catalog/']

    def __init__(self, category=None, *args, **kwargs):
        super(DnsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.dns-shop.ru/catalog/{category}']
        # print(args)

    def parse(self, response):
        names = response.css(".catalog-product__name::text").extract()
        prices = response.css(".product-buy__price::text").extract()
        for i in zip(names, prices):
            item = ParseItem()
            item['name'] = i[0]
            item['price'] = i[1].replace("\n", "").replace(" ", "")
            yield item


