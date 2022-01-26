import os
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from datetime import datetime, date


class CsvWriterPipeline:

    """Класc, используемый scrapy для записи спарсенных данных в csv файл."""

    @classmethod
    def from_crawler(cls, crawler):
        """Метод, используемый scrapy для создания экземпляра объекта.

        Args:
            crawler:
                паук scrapy.Spider.

        Returns:
            pipeline:
                экземпляр класса.
        """
        pipeline = cls()
        cls.current_date = str(date.today())
        cls.current_time = datetime.now().strftime('_time(%H-%M-%S)')
        cls.auto_parse = crawler.settings['AUTO_PARSE']
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        """Метод, создающий необходимые директории и открывающий необходимые файлы после открытия паука.

        Args:
            spider:
                scrapy.Spider, паук.
        """
        try:
            if spider.custom_settings.get('AUTO_PARSE'):
                os.makedirs(f'parsed_data/{self.current_date}/auto/')
            else:
                os.mkdir(f'parsed_data/{self.current_date}')
        except FileExistsError:
            pass
        finally:
            if spider.custom_settings.get('AUTO_PARSE'):
                self.file = open(f'parsed_data/{self.current_date}/auto/{spider.name + self.current_time}.csv', 'w+b')
            else:
                self.file = open(f'parsed_data/{self.current_date}/{spider.name}.csv', 'w+b')
            self.exporter = CsvItemExporter(self.file)
            self.exporter.start_exporting()

    def spider_closed(self, spider):
        """Метод, завершающий процесс экспорта после закрытия паука.

        Args:
            spider:
                scrapy.Spider, паук.
        """
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        """Метод, завершающий процесс экспорта после закрытия паука

        Args:
            item:
                спарсенные данные.
            spider:
                scrapy.Spider, паук.

        Returns:
            item:
                спарсенные данные
        """
        self.exporter.export_item(item)
        return item
