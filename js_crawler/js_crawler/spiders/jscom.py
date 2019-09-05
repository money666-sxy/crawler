# -*- coding: utf-8 -*-
import time
import json
import re

import scrapy
from scrapy import Request, FormRequest

from js_crawler.items import JsCrawlerItem


class JscomSpider(scrapy.Spider):
    name = 'jscom'
    allowed_domains = ['jianshu.com']
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Accept': "application/json"}
    start_urls = []
    for i in range(10):
        start_urls.append(
            'https://www.jianshu.com/search/do?q=Python&type=note&page=' + str(i) + '&order_by=default')

    def start_requests(self):
        for url in self.start_urls:
            yield FormRequest(url, callback=self.parse, method="POST", headers=self.headers)

    def parse(self, response):
        # articles = response.xpath(
        #     "//ul[@class='note-list']/li")
        datas = json.loads(response.body)
        # 49个 < em class = 'search-result-highlight' > Python < /em > 学习必备资源，附链接 | 收藏
        articals = datas['entries']
        for artical in articals:
            title = title_fix(artical['title'])
            content = title_fix(artical['content'])
            print("title: ", title)
            print("content: ", content)


def title_fix(title):
    title = title.replace(
        r"<em class='search-result-highlight'>", "").replace(r"</em>", "")
    return title


if __name__ == "__main__":
    url = 'https://www.jianshu.com/search/do?q=Python&type=note&page=1&order_by=default'
    import requests
    data = requests.post(url=url, headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'})
    print(data)
