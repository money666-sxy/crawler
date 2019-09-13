import time

import redis
from threading import Thread


class RedisHandler(object):
    def __init__(self):
        self.__conn = redis.Redis(host="localhost", port=6379)
        self.chan_sub = "crawler" # 订阅频道

    def publish(self, msg):
        '''发布'''
        self.__conn.publish(self.chan_sub, msg)
        return True

    def subscribe(self):
        '''订阅'''
        while True:
            pub = self.__conn.pubsub()
            pub.subscribe(self.chan_sub)
            for item in pub.listen():
                if item['type'] == 'pmessage' or item['type'] == 'message':
                    print(item['data'])
            time.sleep(1)

if __name__ == "__main__":
    rd = RedisHandler()
    thread_subscribe = Thread(target=rd.subscribe)
    thread_publish = Thread(target=rd.publish, args=("hello world",))
    thread_subscribe.start()
    thread_publish.start()

