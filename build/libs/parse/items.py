import scrapy


class ProductItem(scrapy.Item):

    """Класс, описывающий спарсенные данные.
    Наследует scrapy.Item."""
    # Имя товара
    name = scrapy.Field()
    # Цена
    price = scrapy.Field()
    # Магазин
    store = scrapy.Field()
    # Ссылка на товар
    url = scrapy.Field()
