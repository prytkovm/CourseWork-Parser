import os
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from datetime import date


class CsvWriterPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        cls.current_date = str(date.today())
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        os.chdir('parsed_data')
        os.mkdir(f'{self.current_date}')
        os.chdir(self.current_date)
        self.file = open(f'{spider.name}.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
