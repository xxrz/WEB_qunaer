# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QunaerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    #创建数据结构
    title = scrapy.Field()
    level = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    province = scrapy.Field()
    string = scrapy.Field()
    intro = scrapy.Field()
    price = scrapy.Field()
    hot_num = scrapy.Field()