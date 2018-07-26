import scrapy
import jsonpath
import re
import json
import datetime
from ..items import ShoppingItem
class TbSpider(scrapy.Spider):
    name = 'tb'
    start_urls = ['https://www.taobao.com/']

    custom_settings = {
        'ITEM_PIPELINES' : {
           'shopping.pipelines.ShoppingPipeline': 300,
            'shopping.pipelines.ShoppingImagePipeline' :1
        }
    }


    def parse(self, response):
        url = "https://s.taobao.com/search?q=男装&s=%d"
        for i in range(1,2):
            shop_list_url = url % ((i-1) * 44)
            # print(shop_list_url)
            yield scrapy.Request(shop_list_url,callback=self.get_shop_list)

    def get_shop_list(self,response):
        html = response.text
        connect_pat = re.compile('g_page_config = (.*);\n')

        connect = connect_pat.search(html)
        if connect:
            connects = json.loads(connect.group(1))
            shop_list = jsonpath.jsonpath(connects,'$..auctions.*')
            for shop in shop_list:
                item = ShoppingItem()
                shop_name = shop['raw_title']
                shop_title = shop['title']
                shop_price = shop['view_price']
                shop_comment = shop['comment_count']
                shop_seller = shop['nick']
                tags = shop['icon']
                tags_list = []
                if tags:
                    for tag in tags:
                        tags_list.append(tag['title'])

                shop_tags = ','.join(tags_list)
                shop_img_url = []
                img_url = 'https:' + shop['pic_url']
                shop_img_url.append(img_url)

                shop_url = "https:" +  shop['detail_url']


                item['shop_url'] = shop_url

                item['shop_img_url'] = shop_img_url

                item['shop_name'] = shop_name

                item['shop_price'] = shop_price

                item['shop_title'] = shop_title

                item['shop_comment'] = shop_comment

                item['shop_seller'] = shop_seller

                item['shop_class'] = '男装'

                item['shop_tags'] = shop_tags

                item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                yield item


