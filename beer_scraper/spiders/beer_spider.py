# -*- coding: utf-8 -*-
# Author: Cedric Wang
# Date: May 14, 2018
# Python Version: 3.6.3
# Scrapy Version: 1.5
# Description: This spider goes through every brewery in beeradvocate.com and download all comments
#               for every beer, and the associated info for the beer.
import scrapy
import re
from beer_scraper.items import CommentItem
from beer_scraper.items import BeerInfoItem


class BeerSpiderSpider(scrapy.Spider):
    name = 'beer_comments'
    allowed_domains = ['beeradvocate.com']
    
    start_urls = ['https://www.beeradvocate.com/place/list/?start=0&&brewery=Y&sort=name']

    #this function finds every brewery in the page and goes to the next page
    def parse(self, response):
        for brewery in response.css('td a').re('href="(/beer/profile/.*)">'):
            yield response.follow(brewery, self.parse_brewery)
        
        # next_page =  response.css('a').re('<a href="(.*)">next')
        # if next_page:
        #     next_url = re.sub('&amp;', '&', next_page[0])
        #     yield response.follow(next_url, self.parse)
    
    #this function finds all the beers in breweries page
    def parse_brewery(self, response):
        for beer in response.css('td.hr_bottom_light a').re('href="(/beer/profile/.*)">'):
            yield response.follow(beer, self.parse_comment)
        
    #this function finds all the comments and parse them and stores them as items to be 
    #used in item pipeline for exporting
    def parse_comment(self, response):
        #beer info
        info = BeerInfoItem()
        
        #names and number
        url_text = response.url
        url_list = url_text.split('/')
        info['brewery_number'] = url_list[-3]
        info['beer_number'] = url_list[-2]
        info['brewery_name'] = response.css('h1').re('\| (.*)</s')
        info['beer_name'] =response.css('h1').re('>(.*)<s')

        #getting location data
        location = response.css('#info_box a').re('/place/.*>(.*)</a>')
        info['city'] = location[0]
        info['country'] = location[-1]
        if len(location)>2:
            info['province'] = location[-2]
        
        #style
        style = response.css("div #info_box a b").extract()
        if style:
            style = style[1]
            style = re.sub('<(b|/b)>', '', style)
            info['style'] = style
        info['ABV']=response.css('#info_box').re('/b> (.*%)\n\t\t<br>')
        avail = response.css('#info_box').re('</b>(.*)\n\t\t<br>')
        info['availability'] = avail
        info['notes'] = response.css('#info_box').re('<br>\n\t\t(.*)<br>')
        yield info

        #parsing comments
        for comment in response.css('#rating_fullview_content_2'):
            item = CommentItem()
            item['beer_number'] = url_list[-2]
            item['comment'] = comment.css('#rating_fullview_content_2').extract_first() 
            yield item
       
        #crawling next page if exist
        next_page =  response.css('a').re('<a href="(.*)">next')
        if next_page:
            next_url = re.sub('&amp;', '&', next_page[0])
            yield response.follow(next_url, self.parse_comment)

        


