import scrapy
from ..items import ShoppingItem
import datetime
class MeiLiSpider(scrapy.Spider):
    name = 'ml'
    start_urls = ['http://www.meilishuo.com/']

    custom_settings = {
        'ITEM_PIPELINES' : {
           'shopping.pipelines.ShoppingPipeline': 300,
            'shopping.pipelines.ShoppingImagePipeline': 1
        }
    }

    def parse(self, response):
        url = "http://www.meilishuo.com/search/catalog/10057053?page=%d&action=bags"
        for i in range(1,5):
            shop_page_url = url % i
            yield scrapy.Request(shop_page_url,callback=self.get_shop_list)

    def get_shop_list(self,response):
        shop_detail_list = response.xpath('//ul[@id="product-ul"]/li/a/@href').extract()
        for shop_detail in shop_detail_list:
            yield scrapy.Request(shop_detail,callback=self.get_shop_detail)

    def get_shop_detail(self,response):
        item = ShoppingItem()
        shop_url = response.url
        shop_title = response.xpath('//span[@itemprop="name"]/text()').extract_first()
        shop_name = shop_title
        shop_price = response.xpath('//span[@id="J_NowPrice"]/text()').extract_first().strip('¥')
        if '~' in shop_price:
            shop_price = shop_price.split('~')[0]

        shop_comment = response.xpath('//dd[@class="property-extra fr"]/span[last()]/span/text()').extract_first().strip(' \n')

        shop_img_url = response.xpath('//button[@class="middle"]/img/@src').extract()

        shop_tags = response.xpath('//ul[@class="fl clearfix list"]/li/span/text()').extract()

        shop_tags = ','.join([i.strip(' \n ') for i in shop_tags]).strip(',').replace(',,',',')

        shop_seller = response.xpath('//div[@class="name-wrap clearfix"]/a/@title').extract_first()

        item['shop_url'] = shop_url

        item['shop_img_url'] = shop_img_url

        item['shop_name'] = shop_name

        item['shop_price'] = shop_price

        item['shop_title'] = shop_title

        item['shop_comment'] = shop_comment

        item['shop_seller'] = shop_seller

        item['shop_class'] = '包包'

        item['shop_tags'] = shop_tags

        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yield item


