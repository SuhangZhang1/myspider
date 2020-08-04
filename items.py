# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uid=scrapy.Field()
    uurl=scrapy.Field()
    nickname=scrapy.Field()
    reg_date=scrapy.Field()
    following_count=scrapy.Field()
    fans_count=scrapy.Field()
    influence=scrapy.Field()
    introduce=scrapy.Field()
    visit_count=scrapy.Field()
    post_count=scrapy.Field()
    comment_count=scrapy.Field()
    optional_count=scrapy.Field()
    capacity_circle=scrapy.Field()