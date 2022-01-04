# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
import csv


class CsvWriterPipeline(object):

    # path = "D:\\Projects\\Python\\Parse\\items.csv"
    # file = open(path, "a")
    # writer = csv.writer(file)
    # writer.writerow(["name", "price", "store"])
    # def __init__(self):
        #self.writer = csv.DictWriter(open("D:\\Projects\\Python\\parse\\items.csv", 'w'), dialect='excel', lineterminator='\n', delimiter=',')

    def process_item(self, item, spider):
        self.write_to_csv(item)
        return item

    def write_to_csv(self, item):
        #with open("D:\\Projects\\Python\\Parse\\items.csv", 'a') as CsvFile:
            # writer = csv.DictWriter(CsvFile, fieldnames=item.keys())
            # writer.writeheader()
        self.writer.writerow([item['name'], item['price']])
        #self.writer.writerow([item['name'], item['price']])


# class ParsePipeline:
#     def process_item(self, item, spider):
#         return item