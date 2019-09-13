import time
from threading import Thread

import requests
import json

from info_queues.raw_info_queue import RawInfoQueue
from info_queues.db_queue import DBQueue
from items.article_item import ArticleItem
from tools import text_fix


class Parser(object):
    headers = {'accept': 'application/json',
               'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
               'content-type': 'application/json; charset=utf-8',
               'Referrer Policy': 'no - referrer - when - downgrade',
               }
    raw_info_queue = RawInfoQueue(maxsize=10)
    db_queue = DBQueue(maxsize=10)
    start_urls = []
    start = False

    def __init__(self):
        thread_run = Thread(target=self.run)
        thread_run.start()

    class search_key_word(object):
        '''根据关键字搜索文章'''

        def __init__(self, *keyword):
            self.keyword = keyword
            self.get_cookie()
            self.page_num = self.get_page_num()
            self.add_url()

        def get_page_num(self):
            '''获取页数'''
            url = 'https://www.jianshu.com/search/do?q=' + self.keyword + '&type=note&page=' + '1' + '&order_by=default'
            page_info = requests.post(url=url, headers=Parser.headers).text
            total_pages = json.loads(page_info)['total_pages']
            return total_pages

        def get_cookie(self):
            '''获取cookie'''
            Parser.headers['cookie']: '__yadk_uid=w0mb9fgl9kpuFiJ3Rs6RRUElvmrSsUDB; locale=zh-CN; read_mode=day; default_font=font2; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1568139515,1568141141,1568141179,1568220556; _m7e_session_core=534e3428d00577cfdb9c5780bd81ca62; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216c76867f88368-0263c03cd3d34b-38607701-1296000-16c76867f8954e%22%2C%22%24device_id%22%3A%2216c76867f88368-0263c03cd3d34b-38607701-1296000-16c76867f8954e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22desktop%22%2C%22%24latest_utm_medium%22%3A%22search-recent%22%7D%2C%22first_id%22%3A%22%22%7D; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1568223463; signin_redirect=https%3A%2F%2Fwww.jianshu.com%2Fsearch%3Fq%3Dpython%26page%3D1%26type%3Dnote'

        def add_url(self):
            '''添加待处理的url'''
            time.sleep(0.3)
            for i in range(self.page_num):
                Parser.start_urls.append(
                    'https://www.jianshu.com/search/do?q=' + self.keyword + '&type=note&page=' + str(
                        i) + '&order_by=default')
            # print(Parser.start_urls)
            Parser.start = True


    def run(self):
        '''进程开始运行'''
        while True:
            if not Parser.start:
                time.sleep(0.1)
            else:
                break

        thread_get_info = Thread(target=self.get_info, args=(Parser.start_urls, 'POST'))
        thread_parse_info = Thread(target=self.parse_info)
        thread_save2db = Thread(target=self.save2db)
        thread_get_info.start()
        thread_parse_info.start()
        thread_save2db.start()

    def get_info(self, start_urls, method):
        '''发送请求'''
        try:
            '''请求数据'''
            if method == 'GET':
                for url in start_urls:
                    info = requests.get(url=url, headers=Parser.headers).text
            elif method == 'POST':
                for url in start_urls:
                    try:
                        info = requests.post(url=url, headers=Parser.headers).text
                        Parser.raw_info_queue.put(info)
                        print("put................")
                        time.sleep(2)
                    except:
                        raise Exception("requests" + url + "error")
        except Exception as e:
            print(e)

    def parse_info(self):
        '''处理数据并存入缓冲区'''
        try:
            while True:
                info = Parser.raw_info_queue.get()
                print("get.................")
                try:
                    text = json.loads(info)['entries']
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
                        Parser.db_queue.put(article)
                except:
                    raise Exception("赋值出错")
        except Exception as e:
            print(e)

    def save2db(self):
        '''入库'''
        try:
            while True:
                article_db = Parser.db_queue.get()
                try:
                    print(article_db.title)
                    print(article_db.content)
                    print(article_db.author.id)
                    print(article_db.first_shared_at)
                except:
                    raise Exception("get article_db error")
        except Exception as e:
            print(e)




if __name__ == "__main__":
    # print((datetime.datetime.today() - datetime.datetime(2019, 2, 24)).days)

    parser = Parser()
    parser.search_key_word('python')
