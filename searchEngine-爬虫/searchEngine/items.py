# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SearchengineItem(scrapy.Item):
    title = scrapy.Field()
    source_detail = scrapy.Field()
    source_url = scrapy.Field()
    introduce = scrapy.Field()
    content = scrapy.Field()
    
    