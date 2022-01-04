import scrapy
from ..items import ParseItem
import ast


class CitilinkSpider(scrapy.Spider):

    def __init__(self, sub=None):
        self.name = 'Citilink'
        self.start_urls = [f'https://www.citilink.ru/{sub}']
        super(CitilinkSpider, self).__init__()
        self.current_page = 1

    def parse(self, response):
        names = response.css(".ProductCardHorizontal__title::text").extract()
        prices = response.css(".ProductCardHorizontal__price_current-price::text").extract()
        # У Ситилинка наблюдается разная разметка от страницы к странице, стоит это учитывать
        if names == [] and prices == []:
            cards_data = response.css(".product_data__gtm-js.product_data__pageevents-js.ProductCardVertical"
                                      ".ProductCardVertical_normal"
                                      ".ProductCardVertical_shadow-hover"
                                      ".ProductCardVertical_separated::attr(data-params)").extract()
            for item in cards_data:
                card_dict = ast.literal_eval(item)
                names.append(card_dict['shortName'])
                prices.append(str(card_dict['price']))
        for i in zip(names, prices):
            item = ParseItem()
            item['name'] = i[0]
            item['price'] = i[1].replace("\n", "").replace(" ", "")
            yield item
        self.current_page += 1
        next_page_url = response.css(f'a[data-page=\"{self.current_page}\"]::attr(href)').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
