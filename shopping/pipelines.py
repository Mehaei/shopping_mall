# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.pipelines.images import ImagesPipeline

class ShoppingPipeline(object):
    def open_spider(self,spider):
        self.db = pymysql.connect('127.0.0.1','root','123456','reptile',charset='utf8')
        self.cursor = self.db.cursor()
    def process_item(self, item, spider):

        item['shop_source'] = spider.name
        sql,data = item.get_data()
        try:
            self.cursor.execute(sql,data)
            self.db.commit()
        except Exception as e:
            self.cursor.execute('alter table shop auto_increment=1')
            print(e)
            self.db.rollback()
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()
# 测试中间件
# class ShopingPipeline(object):
#     i = 0
#     def process_item(self,item, spider):
#         print(self.i)
#         self.i += 1
#         return item



class ShoppingImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        # shop_img_path
        img_path = []
        for res in results:
            if res[0]:
                path = res[1]['path'].strip('full/')
                img_path.append(path)
        img_path = ','.join(img_path)
        item['shop_img_path'] = img_path
        return item
