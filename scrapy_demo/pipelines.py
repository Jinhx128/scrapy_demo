# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json


class TestPipeline:
    # def process_item(self, item, spider):
    #     return item
    def __init__(self):
        self.f = open('test.json', 'wb')

    def process_item(self, item, spider):
        if item['title'] != None:  # 过滤掉移动类的帖子
            data = json.dumps(dict(item), ensure_ascii=False, indent=4) + ','
            self.f.write(data.encode('utf-8'))
        return item  # 返回item，告诉引擎，我已经处理好了，你可以进行下一个item数据的提取了

    def close_spider(self, spider):
        self.f.close()

class LuoyublogPipeline:
    # def process_item(self, item, spider):
    #     return item
    def __init__(self):
        self.f = open('luoyublog.json', 'wb')

    def process_item(self, item, spider):
        data = json.dumps(dict(item), ensure_ascii=False, indent=4) + ','
        self.f.write(data.encode('utf-8'))
        return item  # 返回item，告诉引擎，我已经处理好了，你可以进行下一个item数据的提取了

    def close_spider(self, spider):
        self.f.close()
