# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
import csv


class CsvWriterPipeline(object):

    def __init__(self):
        self.writer = csv.writer(open("D:\\Projects\\Python\\Parse\\items.csv", 'w'), lineterminator='\n', delimiter=',')

    def process_item(self, item, spider):
        self.write_to_csv(item)
        return item

    def write_to_csv(self, item):
        self.writer.writerow([item['name'], item['price']])


class ParsePipeline:
    def process_item(self, item, spider):
        return item