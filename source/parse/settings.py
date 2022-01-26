# Файл с настройками проекта scrapy
# Отключаем логгирование
LOG_ENABLED = False
# Имя бота
BOT_NAME = 'parse'
# Используемые в проекте модули с описанием пауков
SPIDER_MODULES = ['parse.spiders']
NEWSPIDER_MODULE = 'parse.spiders'
# Говорим scrapy не следовать правилам в robots.txt
ROBOTSTXT_OBEY = False
# Отключаем куки
COOKIES_ENABLED = False
# Отключаем консоль Telnet
TELNETCONSOLE_ENABLED = False
# Используем сгенерированные scrapy промежуточные ПО, и включаем свои
SPIDER_MIDDLEWARES = {
    'parse.middlewares.SpiderMiddleware': 543,
}
DOWNLOADER_MIDDLEWARES = {
    'parse.middlewares.DownloaderMiddleware': 550,
    'parse.middlewares.RollingUserAgentMiddleware': 343,
    'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610,
    'parse.middlewares.SettingsReaderMiddleware': 570,
}

# Конфигурация для прокси от zyte
ZYTE_SMARTPROXY_ENABLED = False
ZYTE_SMARTPROXY_APIKEY = '32180d6375aa4af8a8d4aec950eeab00'
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 16
DOWNLOAD_TIMEOUT = 600
DEFAULT_REQUEST_HEADERS = {
    "X-Crawlera-Profile": "desktop",
    "X-Crawlera-Cookies": "disable",
}

# Параметры ниже позволяют scrapy отправлять запросы таким образом, чтобы не нагружать сервер и, соответственно, не попадать под бан,
# Активируется только при отключенных прокси
AUTOTHROTTLE_ENABLED = False
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10

# Включаем наше по для экспорта в csv
ITEM_PIPELINES = {
    'parse.pipelines.CsvWriterPipeline': 300,
}

# Частота подмены user-agent
UA_CHANGE_FREQUENCY = 50
# user-agent по умолчанию, устанавливается, если возникла ошибка в fake-user-agent
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
# Сконфигурирован ли автопарсинг
AUTO_PARSE = False
