# -*- coding: utf-8 -*-
import scrapy

from js_crawler.items import JsCrawlerItem


class JscomSpider(scrapy.Spider):
    name = 'jscom'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://jianshu.com']

    def parse(self, response):
        # articles = response.xpath(
        #     "//ul[@class='note-list']/li")
        title = response.xpath(
            "//ul[@class='note-list']//div[@class='content']/a[@class='title']/text()").extract_first()
        author = response.xpath(
            "//ul[@class='note-list']//div[@class='content']//div[@class='meta']//a[@class='nickname']/text()"
        ).extract_first()
        desc = response.xpath(
            "//ul[@class='note-list']//div[@class='content']/p[@class='abstract']/text()").extract_first()

        print("第一篇文章的标题: ", title)
        print("第一篇文章的作者: ", author)
        print("第一篇文章简介: ", desc)

        # for articale in articles:
        #     item = JsCrawlerItem()
        #     item['title'] = articale.xpath(
        #         ".div//[@class='content']/a[@class='title']/text()")
        #     items.append(item)
