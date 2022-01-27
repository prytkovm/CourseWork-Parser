import scrapy
from ..items import ProductItem


class OnlineTradeSpider(scrapy.Spider):

    """Класс, описывающий парсер магазина OnlineTrade.
    Наследует scrapy.Spider.
    """

    def __init__(self, urls=None, parse_multiple_items=False):
        """Конструктор класса OnlineTradeSpider

        Args:
            urls:
                список ссылок для парсинга, по умолчанию None.
            parse_multiple_items:
                флаг, указывающий тип страницы для парсинга (один товар/страница с товарами), по умолчанию False.
        """
        self.name = 'OnlineTrade'
        self.parse_multiple_items = parse_multiple_items
        self.start_urls = urls
        super(OnlineTradeSpider, self).__init__()

    def parse(self, response):
        """Метод, используемый для парсинга товаров со страницы.

        Args:
            response:
                http ответ.
        """
        # Получаем карточки с товарами
        products = response.css('div.indexGoods__item')
        if products.get() is not None:
            for product in products:
                item = ProductItem()
                name = product.css('a.indexGoods__item__name::text').get()
                if name is not None:
                    item['name'] = name
                price = product.css('span.price::text').get()
                if price is not None:
                    item['price'] = price.replace('₽', '')
                url = product.css('a.indexGoods__item__name::attr(href)').get()
                if url is not None:
                    item['url'] = response.urljoin(url)
                item['store'] = 'Online Trade'
                # Отправляем scrapy спарсенный товар, чтоды он его передал в CsvWriterPipeline
                yield item
            # Формуируем ссылку на следующую страницу и говорим scrapy отправить новый запрос
            next_page = response.css('a.js__paginator__linkNext::attr(href)').get()
            if next_page is not None:
                yield scrapy.Request(url=response.urljoin(next_page))

    def extract_product_data(self, response):
        """Метод, используемый для парсинга одного товара.

        Args:
            response:
                http ответ.
        """
        item = ProductItem()
        name = response.css('h1[itemprop="name"]::text').get()
        if name is not None:
            item['name'] = name
        price = response.css('span[itemprop="price"]::text').get()
        if price is not None:
            item['price'] = price
        item['url'] = response.url
        item['store'] = 'Online Trade'
        # Отправляем scrapy спарсенный товар, чтоды он его передал в CsvWriterPipeline
        yield item

    def start_requests(self):
        """Метод, вызываемый scrapy при открытии паука OnlineTradeSpider. Переопределяет метод базового класса."""
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
