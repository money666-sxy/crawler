import time
import threading
from threading import Thread

import requests
import json

from js_crawler.info_queues.raw_info_queue import RawInfoQueue
from js_crawler.info_queues.db_queue import DBQueue
from js_crawler.items.article_item import ArticleItem


class Praser(object):
    def __init__(self, start_urls, headers, method='GET'):
        self.start_urls = start_urls
        self.headers = headers
        self.method = method
        self.raw_info_queue = RawInfoQueue(maxsize=10)
        self.db_queue = DBQueue(maxsize=10)
        thread_get_info = Thread(target=self.get_info)
        thread_parse_info = Thread(target=self.parse_info)
        thread_save2db = Thread(target=self.save2db)
        thread_get_info.start()
        thread_parse_info.start()
        thread_save2db.start()

    def get_info(self):
        '''请求数据'''
        if self.method == 'GET':
            pass
        elif self.method == 'POST':
            for url in self.start_urls:
                info = requests.post(url=url, headers=self.headers).text
                if info is not None:
                    print("exists")
                self.raw_info_queue.put(info)
        else:
            pass

    def parse_info(self):
        '''处理数据并存入缓冲区'''
        while True:
            info = self.raw_info_queue.get()
            try:
                text = json.loads(info)['entries']
                print(text[0])
                for item in text:
                    article = ArticleItem()
                    article.id = item['id']
                    article.title = text_fix(item['title'])
                    article.content = text_fix(item['content'])
                    article.slug = item['slug']
                    article.author.id = item['user']['id']
                    article.author.nickname = item['user']['nickname']
                    article.author.author_avatar_url = item['user']['avatar_url']
                    article.notebook.id = item['notebook']['id']
                    article.notebook.name = item['notebook']['name']
                    article.commentable = item['commentable']
                    article.public_comments_count = item['public_comments_count']
                    article.like_count = item['likes_count']
                    article.views_count = item['views_count']
                    article.total_rewards_count = item['total_rewards_count']
                    article.first_shared_at = item['first_shared_at']
                    print("end........................................")
                    self.db_queue.put(article)
            except:
                # print(json.loads(info))
                print("延长请求时间。。。。。")
                time.sleep(20)
                exit()

    def save2db(self):
        while True:
            article_db = self.db_queue.get()
            if article_db is not None:
                for _ in range(10):
                    print()
            print(article_db.title)
            print(article_db.content)
            print(article_db.author.id)


def text_fix(text):
    text = text.replace(
        r"<em class='search-result-highlight'>", "").replace(r"</em>", "")
    return text


if __name__ == "__main__":
    request_urls = [
        'https://www.jianshu.com/search/do?q=Python&type=note&page=1&order_by=default']
    headers = {'accept': 'application/json',
               'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
               'Referrer Policy': 'no-referrer-when-downgrade'}
    # info = requests.post(url=request_urls[0], headers=headers).text
    # print(info)
    praser = Praser(start_urls=request_urls, headers=headers, method='POST')
