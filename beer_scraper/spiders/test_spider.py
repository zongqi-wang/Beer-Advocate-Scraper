# import scrapy
# import re

# class BeerSpiderSpider(scrapy.Spider):
    
#     num = 0
#     name = 'test_spider'
#     start_urls = ['https://www.beeradvocate.com/place/list/?start=0&&&brewery=Y&sort=name']

#     def parse(self, response):
#         block = response.css("#ba-content tr td.hr_bottom_light b::text").extract()
#         for i in range(1, 20):
#             if int(block[i*4-1])>0:
#                 BeerSpiderSpider.num+=1
        
#         print(BeerSpiderSpider.num)

#         next_page =  response.css('a').re('<a href="(.*)">next')
#         if next_page:
#             next_url = re.sub('&amp;', '&', next_page[0])
#             yield response.follow(next_url, self.parse)