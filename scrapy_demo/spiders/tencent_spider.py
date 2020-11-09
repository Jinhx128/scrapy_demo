# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy_demo.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent_spider'  # 定义爬虫的名称，用于区别spider，该名称必须是唯一的，不可为不同的spider设置相同的名字
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_demo.pipelines.TencentPipeline': 304},
    }
    allowed_domains = ['tencent.com']  # 定义允许爬取的域，若不是该列表内的域名则放弃抓取
    data = {
        'size': 10,
        'page': 1,
        'timestamp': int(time.time() * 1000),
        'keyword': 'java'
    }
    base_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize={}&language=zh-cn&area=cn'.format(data['timestamp'], data['keyword'], data['page'], data['size'])
    start_urls = [base_url]  # spider在启动时爬取的入口url列表，后续的url从初始的url抓取到的数据中提取

    def parse(self,response):  # 定义回调函数，每个初始url完成下载后生成的response对象会作为唯一参数传递给parse()函数。负责解析数据、提取数据（生成Item）、以及生成需要进一步处理的url
        print(response.json())
        data = response.json()['Data']
        articles = data['Posts']
        total = data['Count']
        for article in articles:
            item = TencentItem()
            item['id'] = article['Id']
            item['post_id'] = article['PostId']
            item['recruit_post_id'] = article['RecruitPostId']
            item['recruit_post_name'] = article['RecruitPostName']
            item['country_name'] = article['CountryName']
            item['location_name'] = article['LocationName']
            item['bgname'] = article['BGName']
            item['product_name'] = article['ProductName']
            item['category_name'] = article['CategoryName']
            item['responsibility'] = article['Responsibility']
            item['last_update_time'] = article['LastUpdateTime']
            item['post_url'] = article['PostURL']
            item['source_id'] = article['SourceID']
            item['is_collect'] = article['IsCollect']
            item['is_valid'] = article['IsValid']
            yield item
        if self.data['size'] * self.data['page'] < total:
            self.data['page'] += 1
            self.data['timestamp'] = int(time.time() * 1000)
            yield scrapy.Request('https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize={}&language=zh-cn&area=cn'.format(self.data['timestamp'], self.data['keyword'], self.data['page'], self.data['size']), callback=self.parse)