# flake8: noqa
import random


class Vocab:
    def __init__(self, pool):
        self.pool = pool
        self.idx = 0

    def gen(self):
        return random.choice(self.pool)

    def cycle(self):
        idx = self.idx
        self.idx += 1
        if self.idx == len(self.pool):
            self.idx = 0
        return self.pool[idx]


start_comment = Vocab(
    ['好的，我开始记录～'
    ,'嗯'
    ,'说'
    ])

broken = Vocab(
    ['啊啊啊啊，一定是我坏掉了😱\n或者是你坏掉了😱'
    ,'你要找的东西不存在啊'
    ])

acknowledge = Vocab(
    ['好'
    ,'好[Coffee]'
    ,'收到[Smart]'
    ,'收到～'
    ,'收到[Loafer]'
    ,'好的'
    ,'好的[Coffee]'
    ,'好的[Loafer]'
    ,'好的[Smart]'
    ,'好的[OK]'
    ,'嗯'
    ,'[OK]'
    ])
