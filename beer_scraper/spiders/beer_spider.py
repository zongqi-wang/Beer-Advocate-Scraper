# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class BeerSpiderSpider(scrapy.Spider):
    name = 'beer_comments'
    allowed_domains = ['beeradvocate.com']

    ###########################################################################
    # Description: This function gets all the beer
    def start_requests(self):
        start_urls = [
            'http://www.beeradvocate.com/beer/profile/100',
            'http://www.beeradvocate.com/beer/profile/1',
        ]
        for brewerynumber in range(1,10):
            start_urls.append(f'http://www.beeradvocate.com/beer/profile/{brewerynumber}')

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for url in response.css('td.hr_bottom_light a').re('"(.*profile.*)"'):
            yield response.follow(url, self.parse_comment)

    
    def parse_comment(self, response):
        for comment in response.css('#rating_fullview_content_2'):
            yield{
                'brewery_name': response.css('h1').re('> (.*)</s'),
                'beer_name': response.css('h1').re('>(.*)<s'),
                'comment': comment.css('#rating_fullview_content_2').extract(),
            }

        


