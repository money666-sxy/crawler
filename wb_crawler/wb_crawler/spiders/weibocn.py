# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from wb_crawler.items import UserItem


class WeibocnSpider(scrapy.Spider):
    name = 'weibocn'
    allowed_domains = ['m.weibo.cn']
    start_urls = ['http://m.weibo.cn/']
    # 用户详情
    user_url = "https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}"
    # 关注列表
    follow_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'
    # 粉丝列表
    fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&page={page}'
    # 微博列表
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&page={page}&containerid=107603{uid}'
    start_users = ['3217179555', '1742566624', '2282991915',
                   '1288739185', '3952070245', '5878659096']

    def start_requests(self):
        for uid in self.start_users:
            yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

    def parse_user(self, response):
        '''解析用户信息'''
        result = json.loads(response.text)
        if result.get('data').get('userInfo'):
            user_info = result.get('data').get('userInfo')
            user_item = UserItem()
            field_map = {
                'id': 'id', 'name': 'screen_name', 'avatar': 'profile_image_url', 'cover': 'cover_image_phone',
                'gender': 'gender', 'description': 'description', 'fans_count': 'followers_count',
                'follows_count': 'follow_count', 'weibos_count': 'statuses_count', 'verified': 'verified',
                'verified_reason': 'verified_reason', 'verified_type': 'verified_type'
            }

        for field, attr in field_map.items():
            user_item[field] = user_info.get(attr)
        yield user_item

        # 关注
        uid = user_info.get('id')
        yield Request(self.follow_url.format(uid=uid, page=1), callback=self.parse_follows,
                      meta={'page': 1, 'uid': uid})

        # 粉丝
        yield Request(self.fan_url.foramt(uid=uid, page=1), callback=self.parse_fans,
                      meta={'page': 1, 'uid': uid})

        # 微博
        yield Request(self.weibo_url.format(uid=uid, page=1), callback=self.parse_weibos,
                      meta={'page': 1, 'uid': uid})

    def parse_fans(self, response):
        pass

    def parse_weibos(self, response):
        pass

    def parse(self, response):
        self.logger.debug(response)
        pass


if __name__ == "__main__":
    field_map = {
        'id': 'id', 'name': 'screen_name', 'avatar': 'profile_image_url', 'cover': 'cover_image_phone',
        'gender': 'gender', 'description': 'description', 'fans_count': 'followers_count',
        'follows_count': 'follow_count', 'weibos_count': 'statuses_count', 'verified': 'verified',
        'verified_reason': 'verified_reason', 'verified_type': 'verified_type'
    }
    print(field_map.items())
