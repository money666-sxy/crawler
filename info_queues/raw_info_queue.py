from queue import Queue


class RawInfoQueue(object):
    def __init__(self, maxsize):
        self.cq = Queue(maxsize=maxsize)

    def isEmpty(self):
        return self.cq.empty()

    def isFull(self):
        return self.cq.full()

    def put(self, text):
        self.cq.put(text)

    def get(self):
        return self.cq.get()
