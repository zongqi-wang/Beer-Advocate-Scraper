import scrapy
import re
from beer_scraper.items import BeerInfoItem

class BeerInfoSpiderSpider(scrapy.Spider):

    name = 'beer_info'
    allowed_domains = ['beeradvocate.com']
    start_urls = ['https://www.beeradvocate.com/place/list/?start=0&&brewery=Y&sort=name']

    def parse(self, response):
        for brewery in response.css('a').re('href="(/beer/profile/.*)">'):
            yield response.follow(brewery, self.parse_brewery)
        
        next_page =  response.css('a').re('<a href="(.*)">next')
        if next_page:
            next_url = re.sub('&amp;', '&', next_page[0])
            yield response.follow(next_url, self.parse)
    
    def parse_brewery(self, response):
        for beer in response.css('td.hr_bottom_light a').re('href="(/beer/profile/.*)">'):
            yield response.follow(beer, self.parse_comment)
        

    def parse_comment(self, response):
        info = BeerInfoItem()
        url_text = response.url
        url_list = url_text.split('/')
        info['brewery_number'] = url_list[-3]
        info['beer_number'] = url_list[-2]
        info['brewery_name'] = response.css('h1').re('\| (.*)</s')
        info['beer_name'] =response.css('h1').re('>(.*)<s')
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