# -*- coding: utf-8 -*-
import scrapy
from scrapy_demo.items import BaiduItem


class TestingSpiderSpider(scrapy.Spider):
    name = 'baidu_spider'  # 定义爬虫的名称，用于区别spider，该名称必须是唯一的，不可为不同的spider设置相同的名字
    allowed_domains = ['image.baidu.com']  # 定义允许爬取的域，若不是该列表内的域名则放弃抓取
    base_url = 'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=%E5%88%80%E5%89%91%E7%A5%9E%E5%9F%9F'
    page = 1
    start_urls = [base_url + str(page)]  # spider在启动时爬取的入口url列表，后续的url从初始的url抓取到的数据中提取
    base_link = 'http://bbs.51testing.com/'

    def parse(self, response):  # 定义回调函数，每个初始url完成下载后生成的response对象会作为唯一参数传递给parse()函数。负责解析数据、提取数据（生成Item）、以及生成需要进一步处理的url
        node_list = response.xpath('//*[@id="imgid"]/div/ul')
        totalpage = response.xpath('//a[@class="bm_h"]/@totalpage').extract()[0]
        for node in node_list:
            item = ScrapydemoItem()  # 类型是list
            item['style'] = node.xpath('.//th[@class="common"]/em/a/text()').extract()[0] \
                if len(node.xpath('.//th[@class="common"]/em/a/text()')) else None
            item['title'] = node.xpath('.//th/em/following-sibling::a[1]/text()').extract()[0] \
                if len(node.xpath('.//th/em/following-sibling::a[1]/text()')) else None
            item['link'] = self.base_link + node.xpath('.//th/em/following-sibling::a[1]/@href').extract()[0] \
                if len(node.xpath('.//th/em/following-sibling::a[1]/@href')) else None
            item['author'] = node.xpath('.//td[@class="by"]//cite/a/text()').extract()[0] \
                if len(node.xpath('.//td[@class="by"]//cite/a/text()')) else None
            item['date'] = node.xpath('.//td[@class="by"]//em/span/text()').extract()[0] \
                if len(node.xpath('.//td[@class="by"]//em/span/text()')) else None
            item['response'] = node.xpath('.//td[@class="num"]//a/text()').extract()[0] \
                if len(node.xpath('.//td[@class="num"]//a/text()')) else None
            item['look'] = node.xpath('.//td[@class="num"]//em/text()').extract()[0] \
                if len(node.xpath('.//td[@class="num"]//em/text()')) else None
            yield item  # 返回item（列表），return会直接退出程序，这里是有yield

        if self.page < int(totalpage):
            self.page += 1
            yield scrapy.Request(self.base_url + str(self.page), callback=self.parse)  # 返回请求，请求回调parse，此处也是是有yield