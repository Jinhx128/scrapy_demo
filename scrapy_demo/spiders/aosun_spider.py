# -*- coding: utf-8 -*-
import scrapy
from scrapy_demo.items import AosunItem


class AosunSpider(scrapy.Spider):
    name = 'aosun_spider'  # 定义爬虫的名称，用于区别spider，该名称必须是唯一的，不可为不同的spider设置相同的名字
    # allowed_domains = ['www.aosun.cloud']  # 定义允许爬取的域，若不是该列表内的域名则放弃抓取
    formdata = {
        'page': 1,
        'rows': 4,
        'total': 23,
        'pageTotal': '',
        'isPrivate': False
    }
    total = formdata['page'] * formdata['rows']
    base_url = 'http://aosun.cloud/api/article/getArticleList'
    start_urls = [base_url]  # spider在启动时爬取的入口url列表，后续的url从初始的url抓取到的数据中提取

    def start_requests(self):
        # 发送post请求
        yield scrapy.FormRequest(url=self.start_urls[0], formdata=self.formdata, callback=self.parse)

    def parse(self, response):  # 定义回调函数，每个初始url完成下载后生成的response对象会作为唯一参数传递给parse()函数。负责解析数据、提取数据（生成Item）、以及生成需要进一步处理的url
        print(response)
        # node_list = response.xpath('//*[@class="article"]')
        # totalpage = response.xpath('//a[@class="bm_h"]/@totalpage').extract()[0]
        # for node in node_list:
        #     item = ScrapydemoItem()  # 类型是list
        #     item['style'] = node.xpath('.//th[@class="common"]/em/a/text()').extract()[0] \
        #         if len(node.xpath('.//th[@class="common"]/em/a/text()')) else None
        #     yield item  # 返回item（列表），return会直接退出程序，这里是有yield
        #
        # if self.total < int(totalpage):
        #     self.formdata['page'] += 1
        #     yield scrapy.Request(self.base_url, method='POST', body=self.formdata, callback=self.parse)  # 返回请求，请求回调parse，此处也是是有yield