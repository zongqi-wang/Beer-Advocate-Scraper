import scrapy
import re
from beer_scraper.items import CommentItem
from beer_scraper.items import BeerInfoItem
from beer_scraper.items import BreweryInfoItem


class BeerSpiderSpider(scrapy.Spider):
    
    name = 'test_spider'
    start_urls = ['https://www.beeradvocate.com/beer/profile/27919/127652/?view=beer&sort=&start=1625']

    def parse(self, response):
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
            item['ba_score'] = comment.css('#rating_fullview_content_2 span.BAscore_norm::text').extract()
            item['rdev'] = comment.css('#rating_fullview_content_2 span').re('0000\;">(.*)</span')
            #scores
            scores = comment.css('#rating_fullview_content_2 span.muted::text').extract_first()
            look = re.search('look: ([0-9\.]*) \|', scores)
            if look:
                item['look'] = look.group(1)

            smell = re.search('smell: ([0-9\.]*) \|', scores)
            if smell:
                item['smell'] = smell.group(1)

            taste = re.search('taste: ([0-9\.]*) \|', scores)
            if taste:
                item['taste'] = taste.group(1)

            feel = re.search('feel: ([0-9\.]*) \|', scores)
            if feel:
                item['feel'] = feel.group(1)
            
            overall = re.search('overall: ([0-9\.]*)', scores)
            if overall:
                item['overall'] = overall.group(1)

            comment_text = comment.css('#rating_fullview_content_2').extract_first()
            comment_text = re.sub('<div id="rating.*</span><br><br>','',comment_text)
            item['comment'] = re.sub('<div><span class.*', '', comment_text)

            item['username'] = comment.css('div#rating_fullview_content_2 span.muted a.username::text').extract()
            item['date'] = comment.css('div#rating_fullview_content_2 span.muted a::text').extract()[1]
            yield item
       
        #crawling next page if exist
        next_page =  response.css('a').re('<a href="(.*)">next')
        if next_page:
            next_url = re.sub('&amp;', '&', next_page[0])
            yield response.follow(next_url, self.parse)
