# -*- coding: utf-8 -*-
import scrapy
from scrapy_demo.items import LuoyublogItem

class LuoyublogSpider(scrapy.Spider):
    name = 'luoyublog_spider'  # 定义爬虫的名称，用于区别spider，该名称必须是唯一的，不可为不同的spider设置相同的名字
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_demo.pipelines.LuoyublogPipeline': 302},
    }
    allowed_domains = ['luoyublog.com']  # 定义允许爬取的域，若不是该列表内的域名则放弃抓取
    data = {
        'latest': 'true',
        'page': 1,
        'limit': 10
    }
    base_url = 'https://luoyublog.com/api/luoyublog/articles?latest={}&page={}&limit={}'.format(data['latest'], data['page'], data['limit'])
    start_urls = [base_url]  # spider在启动时爬取的入口url列表，后续的url从初始的url抓取到的数据中提取

    def parse(self,response):  # 定义回调函数，每个初始url完成下载后生成的response对象会作为唯一参数传递给parse()函数。负责解析数据、提取数据（生成Item）、以及生成需要进一步处理的url
        data = response.json()['page']
        articles = data['list']
        total = data['totalCount']
        for article in articles:
            item = LuoyublogItem()
            item['id'] = article['id']
            item['title'] = article['title']
            item['description'] = article['description']
            item['author'] = article['author']
            item['cover'] = article['cover']
            yield item
        if self.data['limit'] * self.data['page'] < total:
            self.data['page'] += 1
            yield scrapy.Request('https://luoyublog.com/api/luoyublog/articles?latest={}&page={}&limit={}'.format(self.data['latest'], self.data['page'], self.data['limit']), callback=self.parse)