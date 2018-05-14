# -*- coding: utf-8 -*-
import scrapy


class BeerSpiderSpider(scrapy.Spider):
    name = 'beer_comments'
    allowed_domains = ['beeradvocate.com']

    start_urls = ['https://www.beeradvocate.com/beer/']


    def parse(self, response):
        for beer in response.css('#rating_fullview_content_2 h6 a').re('href="(.*)">'):
            yield response.follow(beer, self.parse_comment)
            

    
    def parse_comment(self, response):
        print(response.url)
    #def parse_comment(self, response):
    #    for comment in response.css('#rating_fullview_content_2'):
    #        yield{
    #            'brewery_name': response.css('h1').re('> (.*)</s'),
    #            'beer_name': response.css('h1').re('>(.*)<s'),
    #            'comment': comment.css('#rating_fullview_content_2').extract_first(),
    #        }
    #    
    #    next_page =  response.css('a').re('<a href="(.*)">next')
    #    if next_page:
    #        yield response.follow(next_page[0], self.parse_comment)

        


