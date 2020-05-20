# -*- coding = scrapy.Field() utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in = scrapy.Field()
# https = scrapy.Field()//docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Identity
from w3lib.html import remove_tags


def remove_whitespace(value):
    return value.strip()

class AggroPocItem(scrapy.Item):
    # define the fields for your item here like = scrapy.Field()
    # name = scrapy.Field()
    pass

class JobItem(scrapy.Item):
    employer = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_whitespace),
        output_processor=TakeFirst(),
    )
    position = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_whitespace),
        output_processor=TakeFirst(),
    )
    jobLink = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_whitespace),
        output_processor=TakeFirst(),
    )
    location = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_whitespace),
        output_processor=TakeFirst(),
    )
    urgency = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_whitespace),
        output_processor=TakeFirst(),
    )
    employerRating = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_whitespace),
        output_processor=TakeFirst(),
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_whitespace),
        output_processor=TakeFirst(),
    )
    details = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_whitespace),
        output_processor=Identity(),
    )
