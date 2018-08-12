# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http.response.html import HtmlResponse
import time


class ShoppingDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.


    def process_request(self, request, spider):
        # 避免首次请求使用selenium
        if request.url != 'https://www.jd.com/':
            # 从spider中获取浏览器对象
            spider.browser.get(request.url)

            time.sleep(0.5)
            # 执行js滑动到浏览器底部
            spider.browser.execute_script('$(document).scrollTop($(document).height())')

            time.sleep(2)
            # 获取页面源码
            html = spider.browser.page_source
            # 返回响应
            return HtmlResponse(url=request.url,body=html,request=request,encoding='utf-8')

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
