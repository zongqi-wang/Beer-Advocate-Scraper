# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeerScraperItem(scrapy.Item):
    # define the fields for your item here like:
    beer_name = scrapy.Field()
    beer_number = scrapy.Field() 
    brewery_name = scrapy.Field()
    brewery_number = scrapy.Field()
    comment = scrapy.Field()    

class BeerInfoItem(scrapy.Item):
    beer_name = scrapy.Field()
    beer_number = scrapy.Field() 
    brewery_name = scrapy.Field()
    brewery_number = scrapy.Field()
    style = scrapy.Field()
    ABV = scrapy.Field(()
    availablility = 