import scrapy
from ..items import ShoppingItem
import datetime
import math
from urllib import request
import time
from urllib import parse
from selenium import webdriver
class JingDongSpider(scrapy.Spider):
    name = 'jd'
    start_urls = ['https://www.jd.com/']
    # sign = True
    custom_settings = {
        'ITEM_PIPELINES' : {
           'shopping.pipelines.ShoppingPipeline': 300,
            'shopping.pipelines.ShoppingImagePipeline': 1,
            # 'shopping.pipelines.ShopingPipeline' : 300
        },
         # 使用selenium加载剩余部分数据
         # 'DOWNLOADER_MIDDLEWARES' : {
         #    'shopping.mymiddlewares.ShoppingDownloaderMiddleware': 500,
         # }
    }
    sign = True
    head = {
        "Host": "search.jd.com",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        "Referer": "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=647e94e2fda448c793707bfba6990c5b",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "unpl=V2_ZzNtbUVeQx0hXBQGfx8ODWIKRV0SXxcRJg9EVSgeWgRhBRNZclRCFXwUR11nGV8UZwMZWUpcQRZFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VnkdXgdhAxRbcmdEJUU4RFR4HF0EVwIiXHIVF0l8DENdeB8RB2UHEF9EV0UTRQl2Vw%3d%3d; __jda=122270672.335337177.1534046370.1534046370.1534046371.1; __jdc=122270672; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_6819eecc57c948f1a9e5b630b6707705|1534046370858; __jdu=335337177; shshshfpb=17a1a04e3202f4abdbc3e66fcbce1e493005c208ec1629f935b2f7492c; PCSYCityID=258; shshshfpa=81d4dd31-c936-e5b2-f597-43276a1ba7ef-1534046371; xtest=5941.cf6b6759; ipLoc-djd=1-72-2799-0; rkv=V0900; qrsc=3; shshshfp=e9ed31704547dd4e34dd6ab8ef92534b; 3AB9D23F7A4B3C9B=SLFYRKOQZRB4KGQAJ47E3KAXIZXOBDYYDW3ZLWM4B36VC4OSZ4AQNRUZZH7UEJUEX7AVTIRZBUDU6YLFHWNYTS7EI4; __jdb=122270672.8.335337177|1.1534046371; shshshsID=296f12a7e5c5d6847f4f6d710f187876_8_1534051151877",

    }
    # 在程序开始时，创建浏览器对象，避免每次请求都经过中间件，打开关闭浏览器
    # def __init__(self):
    #     print('spider open')
    #     self.browser = webdriver.PhantomJS(executable_path=r'E:\reptile\software\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    #     # super(JingDongSpider, self).__init__()
    #     super().__init__()
    # # 当程序结束时，关闭浏览器
    # def closed(self,spider):
    #     print('spider closed')
    #     self.browser.close()

    def parse(self, response):
        url = 'https://search.jd.com/Search?keyword=手机&enc=utf-8&page=%d'
        for i in range(1,3,2):
            search_url = url % i
            yield scrapy.Request(search_url,callback=self.get_shopping_list,meta={'i' : i})

            # self.sign = True
    def get_shopping_list(self, response):
        detail_url_list = []
        if self.sign:
            detail_url_list = response.xpath('//div[@id="J_goodsList"]/ul/li[@class="gl-item"]/@data-pid').extract()
            shop_list = response.xpath('//div[@id="J_goodsList"]/ul/li[@class="gl-item"]')
        else:
            shop_list = response.xpath('//li[@class="gl-item"]')

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

        if self.sign:
            i = response.meta['i']
            url = "https://search.jd.com/s_new.php?"
            shopping_id = ','.join(detail_url_list)
            ttime = '%.5f' % time.time()
            data = {
                "keyword": "手机",
                "enc": "utf-8",
                "qrst": "1",
                "rt": "1",
                "stop": "1",
                "vt": "2",
                "wq": "手机",
                "cid2": "653",
                "cid3": "655",
                "page": int(i) + 1,
                "s": "29",
                "scrolling": "y",
                "log_id": ttime,
                "tpl": "3_M",
                "show_items": shopping_id,
            }
            data = parse.urlencode(data)
            two_url = url + data
            yield scrapy.Request(two_url,callback=self.get_shopping_list,headers=self.head)

            self.sign = False











