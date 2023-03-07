from fake_useragent import UserAgent, FakeUserAgentError
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from PyQt6.QtCore import QSettings


class SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed __objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item __objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item __objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed __objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SettingsReaderMiddleware(DownloaderMiddleware):

    """Класс, изменяющий настройки пауков, основываясь на конфигурации, выбранной пользователем.
    Наследует DownloaderMiddleware.
    """

    def spider_opened(self, spider):
        """Метод, вызываемый при открытии паука и изменяющий его конфигурацию.

        Args:
            spider:
                scrapy.Spider, открытый паук
        """
        app_settings = QSettings('parser_config.ini', QSettings.Format.IniFormat)
        if app_settings.value('proxy_enabled', type=bool):
            if app_settings.value('auto_parse', type=bool):
                spider.custom_settings = {
                    'ZYTE_SMARTPROXY_ENABLED': True,
                    'CONCURRENT_REQUESTS': 16,
                    'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
                    'AUTOTHROTTLE_ENABLED': False,
                    'AUTO_PARSE': True
                }
            else:
                spider.custom_settings = {
                    'ZYTE_SMARTPROXY_ENABLED': True,
                    'CONCURRENT_REQUESTS': 16,
                    'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
                    'AUTOTHROTTLE_ENABLED': False,
                    'AUTO_PARSE': False
                }
        else:
            if app_settings.value('auto_parse', type=bool):
                spider.custom_settings = {
                    'ZYTE_SMARTPROXY_ENABLED': False,
                    'CONCURRENT_REQUESTS': 1,
                    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
                    'AUTOTHROTTLE_ENABLED': True,
                    'AUTO_PARSE': True
                }
            else:
                spider.custom_settings = {
                    'ZYTE_SMARTPROXY_ENABLED': False,
                    'CONCURRENT_REQUESTS': 1,
                    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
                    'AUTOTHROTTLE_ENABLED': True,
                    'AUTO_PARSE': False
                }
        spider.logger.info('Spider opened: %s' % spider.name)


class RollingUserAgentMiddleware(UserAgentMiddleware):

    """Класс, использумый для подмены user-agent при запросах.
    Наследует scrapy.downloadermiddlewares.UserAgentMiddleware.
    """

    @classmethod
    def from_crawler(cls, crawler):
        """Переопределение метода базового класса, используется scrapy для создания экземпляра объекта.

        Args:
            crawler:
                scrapy.Spider, паук.

        Returns:
            pipeline:
                экземпляр класса
        """
        middleware = cls(crawler.settings['USER_AGENT'])
        cls.requests_count = 0
        cls.frequency = crawler.settings['UA_CHANGE_FREQUENCY']
        cls.default_ua = crawler.settings['DEFAULT_USER_AGENT']
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        return middleware

    def process_request(self, request, spider):
        """Переопределение метода базового класса, вызывается scrapy перед отправкой запроса."""
        if self.requests_count % self.frequency == 0:
            try:
                user_agent = UserAgent()
                user_agent = user_agent.random
            except FakeUserAgentError:
                user_agent = self.default_ua
            request.headers.setdefault('User-Agent', user_agent)
            spider.log('User-Agent: {} {}'.format(request.headers.get('User-Agent'), request))
            self.requests_count += 1
