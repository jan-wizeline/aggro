# -*- coding = scrapy.Field() utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in = scrapy.Field()
# https = scrapy.Field()//docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AggroPocItem(scrapy.Item):
    # define the fields for your item here like = scrapy.Field()
    # name = scrapy.Field()
    pass

class JobItem(scrapy.Item):
    employer = scrapy.Field()
    position = scrapy.Field()
    jobLink = scrapy.Field() 
    location = scrapy.Field() 
    urgency = scrapy.Field() 
    employerRating = scrapy.Field() 
    description = scrapy.Field() 
    details = scrapy.Field() 
