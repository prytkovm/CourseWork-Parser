from PyQt6.QtCore import QRunnable
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from ..spiders.Citilink import CitilinkSpider
from ..spiders.EKatalog import EkatalogSpider
from ..spiders.OnlineTrade import OnlineTradeSpider
from ..tools.communication import Communicate


class ParsingWorker(QRunnable):

    """Класс, описывающий задачу парсинга, исполняемую в отдельном потоке.
    Наследует QRunnable.
    """

    # Статическая переменная для запоминания состояния reactor пакета twisted
    reactor_running = False

    def __init__(self, communicate=Communicate(), urls=None, auto_parse=False):
        """Конструктор класса ParsingWorker.

        Args:
            communicate: объект класса Communicate с описанием сигналов,
            urls: ссылки для парсинга. Представляет собой либо список словарей сгруппированных по магазинам и типу ссылок,
            либо один словарь такого же типа, по умолчанию имеет значение None.
            auto_parse: флаг, указывающий используется ли автопарсинг, по умолчанию False
        """
        super(ParsingWorker, self).__init__()
        self.signals = communicate
        self.urls = urls
        self.auto_parse_enabled = auto_parse
        self.signals.stop_parsing.connect(self.stop_reactor)

    def run(self):
        """Метод, переопределяющий метод родительского класа.
        Запускает задачу в зависимости от значения переданного в конструктор параметра auto_parse:
            True - вызывается метод auto_parse
            False - вызывается метод parse
        """
        if ParsingWorker.reactor_running:
            self.stop_reactor()
        if self.urls is not None:
            if self.auto_parse_enabled:
                self.auto_parse()
            else:
                self.parse()

    def auto_parse(self):
        """Метод, вызываемый, если параметр auto_parse имеет значение True.
        Посылает сигналы parsing_started при запуске пауков и parsing_finished по окончании выполения.
        """
        runner = CrawlerRunner(settings=get_project_settings())
        for links_set in self.urls:
            if links_set['citilink']['product']:
                runner.crawl(CitilinkSpider, urls=links_set['citilink']['product'])
            if links_set['citilink']['products']:
                runner.crawl(CitilinkSpider, parse_multiple_items=True, urls=links_set['citilink']['products'])
            if links_set['e-katalog']['product']:
                runner.crawl(EkatalogSpider, urls=links_set['e-katalog']['product'])
            if links_set['e-katalog']['products']:
                runner.crawl(EkatalogSpider, parse_multiple_items=True, urls=links_set['e-katalog']['products'])
            if links_set['onlinetrade']['product']:
                runner.crawl(OnlineTradeSpider, urls=links_set['onlinetrade']['product'])
            if links_set['onlinetrade']['products']:
                runner.crawl(OnlineTradeSpider, parse_multiple_items=True, urls=links_set['onlinetrade']['products'])
        deferred = runner.join()
        self.signals.parsing_started.emit()
        ParsingWorker.reactor_running = True
        deferred.addBoth(lambda _: self.stop_reactor())
        reactor.run()
        runner.stop()

    def parse(self):
        """Метод, вызываемый, если параметр auto_parse имеет значение True.
        Посылает сигналы parsing_started при запуске пауков и parsing_finished по окончании выполнения.
        """
        runner = CrawlerRunner(settings=get_project_settings())
        if self.urls['citilink']['product']:
            runner.crawl(CitilinkSpider, urls=self.urls['citilink']['product'])
        if self.urls['citilink']['products']:
            runner.crawl(CitilinkSpider, parse_multiple_items=True, urls=self.urls['citilink']['products'])
        if self.urls['e-katalog']['product']:
            runner.crawl(EkatalogSpider, urls=self.urls['e-katalog']['product'])
        if self.urls['e-katalog']['products']:
            runner.crawl(EkatalogSpider, parse_multiple_items=True, urls=self.urls['e-katalog']['products'])
        if self.urls['onlinetrade']['product']:
            runner.crawl(OnlineTradeSpider, urls=self.urls['onlinetrade']['product'])
        if self.urls['onlinetrade']['products']:
            runner.crawl(OnlineTradeSpider, parse_multiple_items=True, urls=self.urls['onlinetrade']['products'])
        self.signals.parsing_started.emit()
        deferred = runner.join()
        self.signals.parsing_started.emit()
        ParsingWorker.reactor_running = True
        deferred.addBoth(lambda _: self.stop_reactor())
        reactor.run()

    def stop_reactor(self):
        """Метод для остановки twisted.reactor."""
        # Своего рода костыль, но по всей видимости единственный механизм, позволяющий перезапустить
        # twisted.reactor и запускать пауков пакета parser.spiders несколько раз без перезапуска приложения
        if ParsingWorker.reactor_running:
            try:
                ParsingWorker.reactor_running = False
                reactor.crash()
            except RuntimeError:
                pass
            except Exception:
                pass
            finally:
                self.signals.parsing_finished.emit(self.auto_parse_enabled)
