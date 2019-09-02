# -*- coding: utf-8 -*-
import scrapy


class WeibocnSpider(scrapy.Spider):
    name = 'weibocn'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://weibo.cn/']

    def parse(self, response):
        pass
