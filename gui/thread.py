# -*- coding: utf-8 -*-
from PyQt5.Qt import (QApplication, QWidget, QPushButton,
                      QThread, QMutex, pyqtSignal)
import sys
import time


class Thread(QThread):
    _signal = pyqtSignal(object)

    def __init__(self, hook=None):
        """
        创建新线程

        :param hook: 设置回调函数
        """
        super(Thread, self).__init__()
        self.hooks = []
        self.set_hook(hook)

    def set_hook(self, hook):
        if callable(hook):
            self.hooks.append(hook)

    def connect(self, func):
        self._signal.connect(func)

    def run(self):
        ret = None
        for hook in self.hooks:
            if callable(hook):
                ret = hook()
            if ret:
                self._signal.emit(ret)

    def test(self, *args, **kwargs):
        print(args, kwargs)

class LoopThread(Thread):
    def __init__(self, hook=None, delay=0):
        super(LoopThread, self).__init__(hook)
        self.delay = delay
        self.flag = True  # 控制循环

    def set_delay(self, delay):
        self.delay = delay

    def stop(self):
        self.flag = False

    def run(self):
        while self.flag:
            ret = None
            for hook in self.hooks:
                if callable(hook):
                    ret = hook()

                if ret:
                    self._signal.emit(ret)

            if self.delay > 0:
                time.sleep(self.delay)

