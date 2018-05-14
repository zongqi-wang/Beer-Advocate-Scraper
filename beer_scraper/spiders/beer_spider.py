# -*- coding: utf-8 -*-
import scrapy
import re
from beer_scraper.items import BeerScraperItem


class BeerSpiderSpider(scrapy.Spider):
    name = 'beer_comments'
    allowed_domains = ['beeradvocate.com']

    start_urls = ['https://www.beeradvocate.com/beer/']


    def parse(self, response):
        for beer in response.css('#rating_fullview_content_2 h6 a').re('href="(.*)">'):
            yield response.follow(beer, self.parse_comment)
        
        #next_page =  response.css('a').re('<a href="(.*)">next')
        #if next_page:
        #    yield response.follow(next_page[0], self.parse)
    
    def parse_comment(self, response):
        for comment in response.css('#rating_fullview_content_2'):
            item = BeerScraperItem()
            url_text = response.url
            url_list = url_text.split('/')
            item['brewery_number'] = url_list[-3]
            item['beer_number'] = url_list[-2]
            item['brewery_name'] = response.css('h1').re('\| (.*)</s')
            item['beer_name'] =response.css('h1').re('>(.*)<s')
            item['comment'] = comment.css('#rating_fullview_content_2').extract_first() 
            yield item
       
        next_page =  response.css('a').re('<a href="(.*)">next')
        #if next_page:
        #    next_url = re.sub('&amp;', '&', next_page[0])
        #    yield response.follow(next_url, self.parse_comment)

        


