import scrapy
from ..items import ProductItem
import re


class EkatalogSpider(scrapy.Spider):

    """Класс, описывающий парсер магазина E-Katalog.
    Наследует scrapy.Spider.
    """

    def __init__(self, urls=None, parse_multiple_items=False):
        """Конструктор класса EkatalogSpider.

        Args:
            urls:
                список ссылок для парсинга, по умолчанию None.
            parse_multiple_items:
                флаг, указывающий тип страницы для парсинга (один товар/страница с товарами), по умолчанию False.
        """
        self.name = 'EKatalog'
        self.parse_multiple_items = parse_multiple_items
        self.start_urls = urls
        super(EkatalogSpider, self).__init__()

    def parse(self, response):
        """Метод, используемый для парсинга товаров со страницы.

        Args:
            response:
                http ответ.
        """
        # Получаем карточки с товарами
        products = response.css('div.tile-item-h')
        # У E-Каталога так же наблюдается различная разметка от страницы к странице
        if products.get() is not None:
            for product in products:
                href = product.css('div.tile-wrapper div.tile-name a.ib::attr(href)').get()
                # Откроем карточку с товаром, чтобы иметь возможность получить больше информации о нем
                if href is not None:
                    yield scrapy.Request(
                        url=response.urljoin(href),
                        callback=self.extract_product_data)
            # Формуируем ссылку на следующую страницу и говорим scrapy отправить новый запрос
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
                            callback=self.extract_product_data
                        )
                next_page = response.css('a.ib.pager-next::attr(href)').get()
                if next_page is not None:
                    yield scrapy.Request(url=response.urljoin(next_page))

    def extract_product_data(self, response):
        """Метод, используемый для парсинга одного товара.

        Args:
            response:
                http ответ.
        """
        table = response.css('div.desc-wbuy table.where-buy-table')
        # Е-каталог присылает всякие непотребства, получим ссылку, используя регулярные выражения
        url_pattern = re.compile('this.href=\"(.+?)\";')
        if table.get() is not None:
            for data in table:
                prices = data.css('td.where-buy-price a::text').extract()
                urls = data.css('td.where-buy-price div.hide-blacked').extract()
                stores = data.css('td.where-buy-description div.hide-blacked a.it-shop::text').extract()
                if prices and urls and stores:
                    for i in zip(prices, stores, urls):
                        item = ProductItem()
                        name = response.css('h1.t2::text').get()
                        item['name'] = name.replace(',', ' ')
                        item['price'] = i[0].replace(u'\xa0', '')
                        item['store'] = i[1]
                        found_url = url_pattern.search(i[2])
                        if found_url:
                            item['url'] = found_url.group(1)
                        else:
                            item['url'] = ''
                        # Отправляем scrapy спарсенный товар, чтоды он его передал в CsvWriterPipeline
                        yield item
        else:
            item = ProductItem()
            item['name'] = response.css('h1.t2::text').get()
            min_price = response.css('span[itemprop="lowPrice"]::text').get()
            max_price = response.css('span[itemprop="highPrice"]::text').get()
            if min_price is not None and max_price is not None:
                item['price'] = min_price.replace(u'\xa0', '') + '-' + max_price.replace(u'\xa0', '')
            elif min_price is not None:
                item['price'] = min_price.replace(u'\xa0', '')
            else:
                item['price'] = 'Не указана'
            item['store'] = 'E-katalog'
            item['url'] = response.url
            # Отправляем scrapy спарсенный товар, чтоды он его передал в CsvWriterPipeline
            yield item

    def start_requests(self):
        """Метод, вызываемый scrapy при открытии паука EKatalogSpider. Переопределяет метод базового класса."""
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
