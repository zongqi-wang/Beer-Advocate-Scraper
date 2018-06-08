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
from beer_scraper.items import BreweryInfoItem

class BeerSpiderSpider(scrapy.Spider):
    name = 'beer_comments'
    allowed_domains = ['beeradvocate.com']
    
    start_urls = ['https://www.beeradvocate.com/place/list/?start=0&&brewery=Y&sort=name']

    ############################################################################
    #this function finds every brewery in the page and goes to the next page
    ############################################################################
    def parse(self, response):
        rows = response.css("#ba-content tr")
        listings = rows.css("td.hr_bottom_light b::text").extract()
        for i in range(0,len(listings)//4):
            if int(listings[i*4+3])>0:
                brewery=rows.css('a').re('href="(/beer/profile/.*)">')[i]
                yield response.follow(brewery, self.parse_brewery)

        next_page =  response.css('a').re('<a href="(.*)">next')
        if next_page:
            next_url = re.sub('&amp;', '&', next_page[0])
            yield response.follow(next_url, self.parse)


    
    #############################################################################   
    #this function finds all the beers in breweries page
    #############################################################################
    def parse_brewery(self, response):
        stats = response.css('#item_stats dd::text').extract()
        #don't record information if 
        # if int(stats) > 0:
        brewery_info = BreweryInfoItem()
        #brewery info
        brewery_info['brewery_name'] = response.css('h1::text').extract()
        brewery_info['brewery_number'] = response.url.split('/')[-2]
        #beer stats
        brewery_info['beers'] = stats[0]
        brewery_info['beer_reviews'] = stats[1]
        brewery_info['beer_ratings'] = stats[2]
        brewery_info['beer_score'] = response.css('#score_box span.ba-ravg::text').extract()
        #brewery stats
        brewery_info['brewery_score'] = response.css('#item_stats dd a::text').extract()
        brewery_info['brewery_review'] = response.css('#item_stats dd span.ba-reviews::text').extract()
        brewery_info['brewery_ratings'] = response.css('#item_stats dd span.ba-ratings::text').extract_first()
        pdev = response.css('#item_stats dd span.ba-pdev::text').extract_first()
        if pdev:
            brewery_info['brewery_pdev'] = re.sub('[\n\t]*', '', pdev)
        #getting location data
        location = response.css('#info_box a').re('/place/.*>(.*)</a>')
        brewery_info['city'] = location[0]
        brewery_info['country'] = location[-1]
        if len(location)>2:
            brewery_info['province'] = location[-2]
        #saving info
        yield brewery_info

        for beer in response.css('td.hr_bottom_light a').re('href="(/beer/profile/.*)">'):
            yield response.follow(beer, self.parse_comment)


    #############################################################################
    #this function finds all the comments and parse them and stores them as items  
    #to be used in item pipeline for exporting
    #############################################################################
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

        
        #style
        style = response.css("div #info_box a b").extract()
        if style:
            style = style[1]
            style = re.sub('<(b|/b)>', '', style)
            info['style'] = style
        info['abv']=response.css('#info_box').re('/b> (.*%)\n\t\t<br>')
        info['availability'] = response.css('#info_box').re('Availability:</b>(.*)\n\t\t')
        info['notes'] = response.css('#info_box').re('<br>\n\t\t(.*)<br>')
        info['ba_score'] = response.css('#score_box span.ba-ravg::text').extract()
        info['ranking'] = response.css('#item_stats dd::text').extract_first()
        info['reviews'] = response.css('#item_stats dd span.ba-reviews::text').extract_first()
        info['ratings'] = response.css('#item_stats dd span.ba-ratings::text').extract_first()
        pdev = response.css('#item_stats dd span.ba-pdev::text').extract_first()
        info['pdev'] = re.sub('[\n\t]*', '', pdev)
        yield info

        #parsing comments
        for comment in response.css('#rating_fullview_content_2'):
            item = CommentItem()
            item['beer_number'] = url_list[-2]
            item['ba_score'] = comment.css('#rating_fullview_content_2 span.BAscore_norm::text').extract ()
            item['rdev'] = comment.css('#rating_fullview_content_2 span').re('0000\;">(.*)</span')
            #scores
            scores = comment.css('#rating_fullview_content_2 span.muted::text').extract_first()
            look = re.search('look: ([0-9\.]*) \|', scores)
            if look is not None:
                item['look'] = look.group(1)

            smell = re.search('smell: ([0-9\.]*) \|', scores)
            if smell is not None:
                item['smell'] = smell.group(1)

            taste = re.search('taste: ([0-9\.]*) \|', scores)
            if taste is not None:
                item['taste'] = taste.group(1)

            feel = re.search('feel: ([0-9\.]*) \|', scores)
            if feel is not None:
                item['feel'] = feel.group(1)
            
            overall = re.search('overall: ([0-9\.]*)', scores)
            if overall is not None:
                item['overall'] = overall.group(1)

            comment_text = comment.css('#rating_fullview_content_2').extract_first()
            comment_text = re.sub('<div id="rating.*</span><br><br>','',comment_text)
            item['comment'] = re.sub('<div><span class.*', '', comment_text)

            item['username'] = comment.css('div#rating_fullview_content_2 span.muted a.username::text').extract()
            item['date'] = comment.css('div#rating_fullview_content_2 span.muted a::text').extract()[-1]
            yield item
       
        #crawling next page if exist
        next_page =  response.css('a').re('<a href="(.*)">next')
        if next_page:
            next_url = re.sub('&amp;', '&', next_page[0])
            yield response.follow(next_url, self.parse_comment)

        




