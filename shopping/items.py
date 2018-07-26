# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShoppingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 商品详情页
    shop_url = scrapy.Field()
    # 商品图片
    shop_img_url = scrapy.Field()
    # 商品名
    shop_name = scrapy.Field()
    # 商品价格
    shop_price = scrapy.Field()
    # 商品标题
    shop_title = scrapy.Field()
    # 商品销量
    shop_comment = scrapy.Field()
    # 店名
    shop_seller = scrapy.Field()
    # 商品亮点
    shop_tags = scrapy.Field()
    # 商品分类
    shop_class = scrapy.Field()
    # 商品本地图片名
    shop_img_path = scrapy.Field()
    # 数据来至于
    shop_source = scrapy.Field()
    # 抓取时间
    crawl_time = scrapy.Field()

    def get_data(self):
        sql = 'insert into shop(name,price,title,comment,seller,tags,shop_class,url,img_path,source,crawl_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        data = (self['shop_name'],self['shop_price'],self['shop_title'],self['shop_comment'],self['shop_seller'],self['shop_tags'],self['shop_class'],self['shop_url'],self['shop_img_path'],self['shop_source'],self['crawl_time'])

        return sql,data