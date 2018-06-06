from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl("comment_spider_1")
process.crawl("comment_spider_2")
process.crawl("comment_spider_3")
process.crawl("comment_spider_4")
process.start()