# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from goldmine.items import GoldmineItem, FinalGoldmineItem 
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
class GoldminePipeline(object):
    def process_item(self, item, spider):

        item_out = FinalGoldmineItem({'category': item['category'], 'name': item['name'], 'address':item['address'], 'telnumber':item['telnumber'], 'email':item['email'], 'logo':item['logo'], 'website':item['website'], 'secondTelnumber': item['secondTelnumber'], 'secondWebsite': item['secondWebsite'], 'secondEmail':item['secondEmail']})
        return self.delete_doubles(item_out)



    def __init__(self):
        self.ids_seen = set()

    def delete_doubles(self, item_out):
    	if item_out['name'] in self.ids_seen:
        	raise DropItem("Duplicate item found: %s" % item_out)
    	else:
        	self.ids_seen.add(item_out['name'])
        	return item_out


class CsvPipeline(object):
    def __init__(self):
        self.file = open("goldmine.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, unicode)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item