# -*- coding: utf-8 -*-
import json
import urllib
import base64

import binascii
import rsa
import scrapy
from scrapy import Request

# from wb_crawler.items import UserItem


class WeibocnSpider(scrapy.Spider):
    name = 'weibocn'
    allowed_domains = ['m.weibo.cn']
    start_urls = ['http://m.weibo.cn/']

    def start_requests(self):
        '''由此处开始爬取'''
        for uid in self.start_users:
            yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

    def parse(self, response):
        self.logger.debug(response)
        pass


def get_su(user_name):
    '''将user_name经过html转义后转成base64编码'''
    username_ = urllib.parse.quote(user_name)  # html字符串转义
    username = base64.encodestring(username_)[:-1]
    return username


def get_sp_rsa(password, servertime, nonce):
    weibo_rsa_n = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
    weibo_rsa_e = 65537
    message = str(servertime) + '\t' + str(nonce) + '\n' + password
    key = rsa.PublicKey(int(weibo_rsa_n, 16), weibo_rsa_e)
    encorpy_pwd = rsa.encrypt(message, key)
    return binascii.b2a_hex(encorpy_pwd)


if __name__ == "__main__":
    print(get_su('15686442131'))
