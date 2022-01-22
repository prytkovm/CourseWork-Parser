import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    store = scrapy.Field()
    url = scrapy.Field()