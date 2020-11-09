# -*- coding: utf-8 -*-
import scrapy
from scrapy_demo.items import AosunItem


class AosunSpider(scrapy.Spider):
    name = 'aosun_spider'  # 定义爬虫的名称，用于区别spider，该名称必须是唯一的，不可为不同的spider设置相同的名字
    allowed_domains = ['aosun.cloud']  # 定义允许爬取的域，若不是该列表内的域名则放弃抓取
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_demo.pipelines.AosunPipeline': 303},
    }
    form_data = {
        'page': '1',
        'rows': '4',
        'isPrivate': 'false'
    }
    total = int(form_data['page']) * int(form_data['rows'])
    base_url = 'http://aosun.cloud/api/article/getArticleList'
    start_urls = [base_url]  # spider在启动时爬取的入口url列表，后续的url从初始的url抓取到的数据中提取
    # headers = {
    #     'Host': 'aosun.cloud',
    #     'Origin': 'http://aosun.cloud',
    #     'Referer': 'http://aosun.cloud/',
    #     'User-Agent:': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    #     'Content-Type': 'application/x-www-form-urlencoded',
    #     'Content-Length': '1149',
    #     'Connection': 'keep-alive',
    #     'Accept': 'application/json, text/plain, */*',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Accept-Language': 'zh-CN,zh;q=0.9'
    # }

    def start_requests(self):
        # 发送post请求
        for url in self.start_urls:
            yield scrapy.FormRequest(url=url, method='POST', formdata=self.form_data, callback=self.parse)

    def parse(self, response):  # 定义回调函数，每个初始url完成下载后生成的response对象会作为唯一参数传递给parse()函数。负责解析数据、提取数据（生成Item）、以及生成需要进一步处理的url
        total = response.json()['total']
        articles = response.json()['info']
        for article in articles:
            item = AosunItem()
            item['id'] = article['id']
            item['title'] = article['title']
            item['modifyrq'] = article['modifyrq']
            item['publish_time'] = article['publishTime']
            item['info'] = article['info']
            item['views'] = article['views']
            item['type_id'] = article['typeId']
            item['is_private'] = article['isPrivate']
            item['state'] = article['state']
            item['info_text'] = article['infoText']
            item['menu_info'] = article['menuInfo']
            item['type'] = article['type']
            yield item
        if int(self.form_data['page']) * int(self.form_data['rows']) < total:
            self.form_data['page'] = str(int(self.form_data['page']) + 1)
            yield scrapy.FormRequest(url=self.start_urls[0], method='POST', formdata=self.form_data, callback=self.parse)