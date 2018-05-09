# -*- coding: utf-8 -*-
import scrapy


class BeerSpiderSpider(scrapy.Spider):
    name = 'beer_comments'
    allowed_domains = ['beeradvocate.com']

    ###########################################################################
    # Description: This function gets all the beer
    def start_requests(self):
        start_urls = [
            'http://www.beeradvocate.com/beer/profile/100'
            'http://www.beeradvocate.com/beer/profile/1'
        ]
        #for brewerynumber in range(1,10):
        #    start_urls.extend(f'http://www.beeradvocate.com/beer/profile/{brewerynumber}')

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_beer)


    def parse_beer(self, response):
        urls = response.css('td.hr_bottom_light a').re('"(.*profile.*)"')

        for url in urls:
            response.follow(url, self.parse_comment)

    
    def parse_comment(self, response):
        for comment in response.css('#rating_fullview_content_2'):
            yield{
                'brewery_name': response.css('h1').re('> (.*)</s'),
                'beer_name': response.css('h1').re('>(.*)<s'),
                'comment': comment.css('#rating_fullview_content_2').extract(),
            }

        


