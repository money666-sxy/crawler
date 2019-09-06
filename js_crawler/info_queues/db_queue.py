from queue import Queue


class DBQueue(object):
    def __init__(self, maxsize):
        self.cq = Queue(maxsize=maxsize)

    def isEmpty(self):
        return self.cq.empty()

    def isFull(self):
        return self.cq.full()

    def put(self, artical_item):
        self.cq.put(artical_item)

    def get(self):
        return self.cq.get()
