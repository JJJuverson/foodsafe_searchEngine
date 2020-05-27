# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from searchEngine.items import SearchengineItem


#class FoodmateSpider(CrawlSpider):
class FoodmateSpider(RedisCrawlSpider):
    name = 'foodmatespider_redis'
    #allowed_domains = ['news.foodmate.net']
    #start_urls = ['http://news.foodmate.net/guonei/list_1.html']
    #lpush foodmatespider:start_urls http://news.foodmate.net/guonei/list_1.html
    redis_key = "foodmatespider:start_urls"

    def __init__(self, *args, **kwargs):
            # Dynamically define the allowed domains list.
            domain = kwargs.pop('domain', '')
            self.allowed_domains = filter(None, domain.split(','))
            super(FoodmateSpider, self).__init__(*args, **kwargs)


    rules = (
        Rule(LinkExtractor(allow=r'.+guonei/list_\d\.html'), follow=True),
        Rule(LinkExtractor(allow=r'.+2020/.+\.html'), callback='parse_detail', follow=False),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@id='title']/text()").get()
        if title==None:
            title = '1'
        source_detail = response.xpath("//div[@class='left_box']/div[@class='info']/text()").get()
        
        source_url = response.xpath("//div[@class='info']/a/@href").get()
        if source_url==None:
            source_url = response.request.url
        introduce = response.xpath("//div[@class='introduce']/text()").get()
        content = response.xpath("//div[@id='content']//text()").getall()
        content = "".join(content).strip()
        item = SearchengineItem(title=title,source_detail=source_detail,source_url=source_url,introduce=introduce,content=content)
        return item
