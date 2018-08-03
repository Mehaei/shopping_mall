import scrapy
from ..items import ShoppingItem
import datetime
import math
from selenium import webdriver
class JingDongSpider(scrapy.Spider):
    name = 'jd'
    start_urls = ['https://www.jd.com/']
    # sign = True
    custom_settings = {
        'ITEM_PIPELINES' : {
           'shopping.pipelines.ShoppingPipeline': 300,
            'shopping.pipelines.ShoppingImagePipeline': 1
        },
         'DOWNLOADER_MIDDLEWARES' : {
            'shopping.mymiddlewares.ShoppingDownloaderMiddleware': 500,
         }
    }

    # 在程序开始时，创建浏览器对象，避免每次请求都经过中间件，打开关闭浏览器
    def __init__(self):
        print('spider open')
        self.browser = webdriver.PhantomJS(executable_path=r'E:\reptile\software\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        # super(JingDongSpider, self).__init__()
        super().__init__()
    # 当程序结束时，关闭浏览器
    def closed(self,spider):
        print('spider closed')
        self.browser.close()

    def parse(self, response):
        url = 'https://search.jd.com/Search?keyword=手机&enc=utf-8&page=%d'
        for i in range(1,3,2):
            search_url = url % i
            yield scrapy.Request(search_url,callback=self.get_shopping_list,meta={'i' : i})
            # self.sign = True

    def get_shopping_list(self,response):

        shop_list = response.xpath('//div[@id="J_goodsList"]/ul/li')
        # print(shop_list)
        print(len(shop_list))

        shop_urll = "https://item.jd.com/%s.html"
        for shop in shop_list:

            item = ShoppingItem()

            sid = shop.xpath('./@data-pid').extract_first()
            shop_url = shop_urll % str(sid)

            shop_img_url_list = shop.xpath('.//div[@class="ps-wrap"]//img/@data-lazy-img').extract()
            shop_img_url = ['https:' + i for i in shop_img_url_list]

            shop_name = shop.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()').extract_first()

            shop_price = shop.xpath('.//div[@class="p-price"]//i/text()').extract_first()

            shop_title = shop.xpath('.//div[@class="p-name p-name-type-2"]/a/@title').extract_first()

            shop_comment = shop.xpath('.//div[@class="p-commit"]/strong/a/text()').extract_first().strip('+')
            if '万' in shop_comment:
                shop_comment = math.floor(float(shop_comment.strip('万')) * 10000)

            shop_seller = shop.xpath('.//div[@class="p-shop"]/span/a/@title').extract_first()

            shop_tags = shop.xpath('.//div[@class="p-icons"]/i/text()').extract()
            shop_tags = ','.join(shop_tags)

            item['shop_url'] = shop_url

            item['shop_img_url'] = shop_img_url

            item['shop_name'] = shop_name

            item['shop_price'] = shop_price

            item['shop_title'] = shop_title

            item['shop_comment'] = shop_comment

            item['shop_seller'] = shop_seller

            item['shop_class'] = '手机'

            item['shop_tags'] = shop_tags

            item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            yield item





















        # for url in detail_url_list:
        #     detail_url = detail % url
        #     yield scrapy.Request(detail_url,callback=self.get_detail)

        # if self.sign:
        #     i = response.meta['i']
        #
        #     shopping_id = ','.join(detail_url_list)
        #     ttime = '%.5f' % time.time()
        #     hz = 's_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=653&cid3=655&page='+str(int(i) +1)+'&log_id='+str(ttime)+'&tpl=3_M&show_items='+shopping_id
        #     two_url = request.urljoin(response.url,hz)
        #     yield scrapy.Request(two_url,callback=self.get_shopping_list)
        #     self.sign = False

    # def get_detail(self,response):
        # shop_url = response.url
        # shop_name = response.xpath('//div[@class="sku-name"]/text()').extract()[-1].strip(' \n')
        # shop_title = response.xpath('//div[@id="p-ad"]/@title').extract()
        # shop_price = response.xpath('//span[@class="p-price"]/span[last()]/text()').extract()
        # shop_combo = response.xpath('//div[@id="choose-attr-2"]/div[@class="dd"]/div/@title').extract()
        # shop_img_url = response.xpath('//div[@id="spec-list"]/ul/li/img/@src').extract()
        #
        # id = shop_url.split('/')[-1].split('.')[0]
        # print(shop_title,shop_price,shop_combo,shop_img_url,id)
        # req_comment = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv28194&productId="+id+"&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1"
        # yield scrapy.Request(req_comment,callback=self.get_comment)
    #
    # def get_comment(self,response):
    #     print(type(json.loads(response.text)),response.text)
