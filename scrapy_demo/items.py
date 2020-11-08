# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TestItem(scrapy.Item):
    # 类型
    style = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 链接
    link = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # 回复
    response = scrapy.Field()
    # 查看
    look = scrapy.Field()


class AosunItem(scrapy.Item):
    # 类型
    style = scrapy.Field()
    # 标题
    title = scrapy.Field()

class BaiduItem(scrapy.Item):
    # 类型
    style = scrapy.Field()
    # 标题
    title = scrapy.Field()

class LuoyublogItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    author = scrapy.Field()
    cover = scrapy.Field()
