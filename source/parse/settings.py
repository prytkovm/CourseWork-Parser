LOG_ENABLED = True
# LOG_LEVEL = 'WARNING'
BOT_NAME = 'parse'

SPIDER_MODULES = ['parse.spiders']
NEWSPIDER_MODULE = 'parse.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False
SPIDER_MIDDLEWARES = {
    'parse.middlewares.SpiderMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = {
    'parse.middlewares.DownloaderMiddleware': 543,
    'parse.middlewares.RollingUserAgentMiddleware': 343,
    'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610
}

# Config for zyte
ZYTE_SMARTPROXY_ENABLED = False
ZYTE_SMARTPROXY_APIKEY = '<PLACE FOR ZYTE API KEY>'
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 16
DOWNLOAD_TIMEOUT = 600
DEFAULT_REQUEST_HEADERS = {
    "X-Crawlera-Profile": "desktop",
    "X-Crawlera-Cookies": "disable",
}

AUTOTHROTTLE_ENABLED = False
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10

ITEM_PIPELINES = {
    'parse.pipelines.CsvWriterPipeline': 300,
}

# Config for UA middleware
UA_CHANGE_FREQUENCY = 50
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
