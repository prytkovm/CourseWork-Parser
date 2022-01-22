import scrapy
from parse.items import ProductItem
import re


class EkatalogSpider(scrapy.Spider):

    def __init__(self, sub=None, parse_item_only=False, parse_goods=False):
        self.name = 'EKatalog'
        self.parse_item_only = parse_item_only
        self.parse_goods = parse_goods
        self.start_urls = [f'https://www.e-katalog.ru/{sub}']
        super(EkatalogSpider, self).__init__()

    def parse(self, response):
        products = response.css('div.tile-item-h')
        if products.get() is not None:
            for product in products:
                href = product.css('div.tile-wrapper div.tile-name a.ib::attr(href)').get()
                if href is not None:
                    yield scrapy.Request(
                        url=response.urljoin(href),
                        callback=self.extract_product_data)
            next_page = response.css('a.ib.pager-next::attr(href)').get()
            if next_page is not None:
                yield scrapy.Request(url=response.urljoin(next_page))
        else:
            products = response.css('div.model-short-div')
            if products.get() is not None:
                for product in products:
                    href = product.css('a.no-u::attr(href)').get()
                    if href is not None:
                        yield scrapy.Request(
                            url=response.urljoin(href),
                            callback=self.extract_product_data)
                next_page = response.css('a.ib.pager-next::attr(href)').get()
                if next_page is not None:
                    yield scrapy.Request(url=response.urljoin(next_page))

    def extract_product_data(self, product):
        table = product.css('div.desc-wbuy table.where-buy-table')
        url_pattern = re.compile('this.href=\"(.+?)\";')
        if table.get() is not None:
            for data in table:
                prices = data.css('td.where-buy-price > a::text').extract()
                urls = data.css('td.where-buy-price div.hide-blacked').extract()
                stores = data.css('td.where-buy-description div.hide-blacked a.it-shop::text').extract()
                if prices and urls and stores:
                    for i in zip(prices, stores, urls):
                        item = ProductItem()
                        name = product.css('h1.t2::text').get()
                        item['name'] = name.replace(',', ' ')
                        item['price'] = i[0].replace(u'\xa0', '')
                        item['store'] = i[1]
                        found_url = url_pattern.search(i[2])
                        if found_url:
                            item['url'] = found_url.group(1)
                        else:
                            item['url'] = ''
                        yield item
        else:
            item = ProductItem()
            item['name'] = product.css('h1.t2::text').get()
            min_price = product.css('span[itemprop="lowPrice"]::text').get()
            max_price = product.css('span[itemprop="highPrice"]::text').get()
            if min_price is not None and max_price is not None:
                item['price'] = min_price.replace(u'\xa0', '') + '-' + max_price.replace(u'\xa0', '')
            elif min_price is not None:
                item['price'] = min_price.replace(u'\xa0', '')
            else:
                item['price'] = 'Не указана'
            item['store'] = 'E-katalog'
            item['url'] = product.url
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
