import scrapy
from ..items import ProductItem


class OnlineTradeSpider(scrapy.Spider):

    def __init__(self, sub=None, parse_item_only=False, parse_goods=False):
        self.name = 'OnlineTrade'
        self.parse_item_only = parse_item_only
        self.parse_goods = parse_goods
        self.start_urls = [f'https://www.onlinetrade.ru/{sub}']
        super(OnlineTradeSpider, self).__init__()

    def parse(self, response):
        products = response.css('div.indexGoods__item')
        if products.get() is not None:
            for product in products:
                item = ProductItem()
                name = product.css('a.indexGoods__item__name::text').get()
                if name is not None:
                    item['name'] = name
                price = product.css('span.price::text').get()
                if price is not None:
                    price.replace('₽', '')
                    item['price'] = price
                url = product.css('a.indexGoods__item__name::attr(href)').get()
                if url is not None:
                    item['url'] = response.urljoin(url)
                item['store'] = 'Online Trade'
                yield item
            next_page = response.css('a.js__paginator__linkNext::attr(href)').get()
            if next_page is not None:
                yield scrapy.Request(url=response.urljoin(next_page))

    def extract_product_data(self, product):
        item = ProductItem()
        name = product.css('h1[itemprop="name"]::text').get()
        if name is not None:
            item['name'] = name
        price = product.css('span[itemprop="price"]::text').get()
        if price is not None:
            item['price'] = price
        item['url'] = product.url
        item['store'] = 'Online Trade'
        yield item

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
