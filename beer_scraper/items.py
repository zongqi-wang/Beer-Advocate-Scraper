# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentItem(scrapy.Item):
    beer_number = scrapy.Field() 
    comment = scrapy.Field()    
    ba_score = scrapy.Field()
    rdev = scrapy.Field()
    look = scrapy.Field()
    smell = scrapy.Field()
    taste = scrapy.Field()
    feel = scrapy.Field()
    overall = scrapy.Field()
    username = scrapy.Field()
    date = scrapy.Field()

class BeerInfoItem(scrapy.Item):
    beer_name = scrapy.Field()
    beer_number = scrapy.Field() 
    brewery_name = scrapy.Field()
    brewery_number = scrapy.Field()
    style = scrapy.Field()
    abv = scrapy.Field()
    availability = scrapy.Field()
    notes = scrapy.Field()
    ba_score = scrapy.Field()
    ranking = scrapy.Field()
    reviews = scrapy.Field()
    ratings = scrapy.Field()
    pdev = scrapy.Field()

class BreweryInfoItem(scrapy.Item):
    brewery_name = scrapy.Field()
    brewery_number = scrapy.Field()
    city = scrapy.Field()
    province = scrapy.Field()
    country = scrapy.Field()
    beers = scrapy.Field()
    beer_reviews = scrapy.Field()
    beer_ratings = scrapy.Field()
    beer_score = scrapy.Field()
    brewery_score = scrapy.Field()
    brewery_review = scrapy.Field()
    brewery_ratings = scrapy.Field()
    brewery_pdev = scrapy.Field()
