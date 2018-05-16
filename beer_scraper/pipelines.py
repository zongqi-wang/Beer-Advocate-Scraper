# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
import csv

class BeerScraperPipeline(object):
    def process_item(self, item, spider):
        return item


def item_type(item):
    return type(item).__name__.replace('Item','').lower()


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if(item_type(item) == 'beerinfo'):
            if item['beer_number'] in self.ids_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.ids_seen.add(item['beer_number'])
                return item
        else:
            return item


class MultiCSVItemPipeline(object):
    SaveTypes = ['comment', 'beerinfo', 'breweryinfo']

    def open_spider(self, spider):
        self.type_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.type_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        name = item_type(item)
        if name not in self.type_to_exporter:
            f = open('{}.csv'.format(name), 'wb')
            exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.type_to_exporter[name] = exporter
        return self.type_to_exporter[name]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
