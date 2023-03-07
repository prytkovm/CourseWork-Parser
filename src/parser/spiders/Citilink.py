import scrapy
from ..items import ProductItem


class CitilinkSpider(scrapy.Spider):

    """Класс, описывающий парсер магазина Citilink.
    Наследует scrapy.Spider.
    """

    def __init__(self, urls=None, parse_multiple_items=False):
        """Конструктор класса CitilinkSpider.

        Args:
            urls:
                список ссылок для парсинга, по умолчанию None.
            parse_multiple_items:
                флаг, указывающий тип страницы для парсинга (один товар/страница с товарами), по умолчанию False.
        """
        if urls is None:
            urls = []
        self.name = 'Citilink'
        self.parse_multiple_items = parse_multiple_items
        self.start_urls = urls
        super(CitilinkSpider, self).__init__()

    def parse(self, response):
        """Метод, используемый для парсинга товаров со страницы.

        Args:
            response:
                http ответ.
        """
        # Получаем карточки с товарами
        products = response.css('div.ProductCardCategoryList__list')
        # У Ситилинка наблюдается различная разметка от страницы к странице, учтем это
        if products.get() is not None:
            for product in products:
                item = ProductItem()
                name = product.css('a.ProductCardHorizontal__title::text').get()
                if name is not None:
                    item['name'] = name
                price = product.css('span.ProductCardHorizontal__price_current-price::text').get()
                if price is not None:
                    item['price'] = price.strip()
                else:
                    item['price'] = 'Нет в наличии'
                item['store'] = 'Citilink'
                url = product.css('a.ProductCardHorizontal__title::attr(href)').get()
                if url is not None:
                    item['url'] = response.urljoin(url)
                # Отправляем scrapy спарсенный товар, чтоды он его передал в CsvWriterPipeline
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
                        item['price'] = price.strip()
                    else:
                        item['price'] = 'Цена не указана'
                    item['store'] = 'Citilink'
                    url = product.css('a.ProductCardVertical__name::attr(href)').get()
                    if url is not None:
                        item['url'] = response.urljoin(url)
                    # Отправляем scrapy спарсенный товар, чтоды он его передал в CsvWriterPipeline
                    yield item
        # Формуируем ссылку на следующую страницу и говорим scrapy отправить новый запрос
        next_page = response.css('a.js--PaginationWidget__page::attr(data-page)')
        if next_page.get() is not None:
            yield scrapy.Request(url=response.urljoin(f'?p={next_page.extract()[-1]}'))

    def extract_product_data(self, response):
        """Метод, используемый для парсинга одного товара.

        Args:
            response:
                http ответ.
        """
        item = ProductItem()
        name = response.css('h1.Heading::text').get()
        item['name'] = name.strip()
        price = response.css('span.ProductHeader__price-default_current-price::text').get()
        if price is not None:
            item['price'] = price.strip()
        else:
            item['price'] = 'Нет в наличии'
        item['store'] = 'Citilink'
        item['url'] = response.url
        # Отправляем scrapy спарсенный товар, чтоды он его передал в CsvWriterPipeline
        yield item

    def start_requests(self):
        """Метод, вызываемый scrapy при открытии паука CitilinkSpider. Переопределяет метод базового класса."""
        if self.start_urls is not None:
            for url in self.start_urls:
                if self.parse_multiple_items:
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse
                    )
                else:
                    yield scrapy.Request(
                        url=url,
                        callback=self.extract_product_data
                    )
