# -*- coding: utf-8 -*-
import scrapy


class BeerSpiderSpider(scrapy.Spider):
    name = 'beer_spider'
    allowed_domains = ['beeradvocate.com']
    start_urls = ['http://beeradvocate.com/']

    def parse(self, response):
        pass
