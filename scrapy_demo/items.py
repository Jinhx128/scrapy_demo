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
    id = scrapy.Field()
    title = scrapy.Field()
    modifyrq = scrapy.Field()
    publish_time = scrapy.Field()
    info = scrapy.Field()
    views = scrapy.Field()
    type_id = scrapy.Field()
    is_private = scrapy.Field()
    state = scrapy.Field()
    info_text = scrapy.Field()
    menu_info = scrapy.Field()
    type = scrapy.Field()

class TencentItem(scrapy.Item):
    id = scrapy.Field()
    post_id = scrapy.Field()
    recruit_post_id = scrapy.Field()
    recruit_post_name = scrapy.Field()
    country_name = scrapy.Field()
    location_name = scrapy.Field()
    bgname = scrapy.Field()
    product_name = scrapy.Field()
    category_name = scrapy.Field()
    responsibility = scrapy.Field()
    last_update_time = scrapy.Field()
    post_url = scrapy.Field()
    source_id = scrapy.Field()
    is_collect = scrapy.Field()
    is_valid = scrapy.Field()

class LuoyublogItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    author = scrapy.Field()
    cover = scrapy.Field()
