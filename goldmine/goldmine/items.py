# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoldmineItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mainurl = scrapy.Field()
    other_url = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    telnumber = scrapy.Field()
    email = scrapy.Field()
    logo = scrapy.Field()
    website = scrapy.Field()

class FinalGoldmineItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    telnumber = scrapy.Field()
    email = scrapy.Field()
    logo = scrapy.Field()
    website = scrapy.Field()
