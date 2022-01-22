import scrapy
from ..items import ProductItem


class CitilinkSpider(scrapy.Spider):

    def __init__(self, sub=None, parse_item_only=False, parse_goods=False):
        self.name = 'Citilink'
        self.parse_item_only = parse_item_only
        self.parse_goods = parse_goods
        self.start_urls = [f'https://www.citilink.ru/{sub}']
        super(CitilinkSpider, self).__init__()

    def parse(self, response):
        products = response.css('div.ProductCardCategoryList__list')
        if products.get() is not None:
            for product in products:
                item = ProductItem()
                name = product.css('a.ProductCardHorizontal__title::text').get()
                if name is not None:
                    item['name'] = name
                price = product.css('span.ProductCardHorizontal__price_current-price::text').get()
                if price is not None:
                    item['price'] = price.rstrip()
                else:
                    item['price'] = 'Нет в наличии'
                item['store'] = 'Citilink'
                url = product.css('a.ProductCardHorizontal__title::attr(href)').get()
                if url is not None:
                    item['url'] = response.urljoin(url)
                yield item
        else:
            products = response.css('div.ProductCardVertical_separated')
            if products.get() is not None:
                for product in products:
                    item = ProductItem()
                    name = product.css('a.ProductCardVertical__name::text').get()
                    if name is not None:
                        item['name'] = name
                    price = product.css('span.ProductCardVerticalPrice__price-current_current-price::text').get()
                    if price is not None:
                        item['price'] = price.rstrip()
                    else:
                        item['price'] = 'Цена не указана'
                    item['store'] = 'Citilink'
                    url = product.css('a.ProductCardVertical__name::attr(href)').get()
                    if url is not None:
                        item['url'] = response.urljoin(url)
                    yield item

        next_page = response.css('a.js--PaginationWidget__page::attr(data-page)')
        if next_page.get() is not None:
            yield scrapy.Request(url=response.urljoin(f'?p={next_page.extract()[-1]}'))

    def extract_product_data(self, product):
        item = ProductItem()
        name = product.css('h1.Heading::text').get()
        item['name'] = ' '.join(name.split()).replace(',', ' ')
        price = product.css('span.ProductHeader__price-default_current-price::text').get()
        if price is not None:
            item['price'] = price
        else:
            item['price'] = 'Нет в наличии'
        item['store'] = 'Citilink'
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