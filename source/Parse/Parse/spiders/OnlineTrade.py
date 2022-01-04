import scrapy
from ..items import ParseItem


class OnlineTradeSpider(scrapy.Spider):

    def __init__(self, sub=None):
        self.name = 'OnlineTrade'
        self.start_urls = [f'https://www.onlinetrade.ru/{sub}']
        super(OnlineTradeSpider, self).__init__()
        self.current_page = 0

    def parse(self, response):
        names = response.css(".indexGoods__item__name::text").extract()
        prices = response.css(".price::text").extract()
        for i in zip(names, prices):
            item = ParseItem()
            item['name'] = i[0]
            item['price'] = i[1].replace("₽", "").replace(" ", "")
            yield item
        paginator_info = response.css(".paginator__count::text").get()
        end = int(paginator_info[paginator_info.find('–') + 1:paginator_info.find('и') - 1])
        count = int(paginator_info[paginator_info.find('з') + 1:])
        self.current_page += 1
        if end != count:
            yield scrapy.Request(response.urljoin(self.start_urls[0] + f'?page={self.current_page}'))

