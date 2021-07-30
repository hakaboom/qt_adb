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
        self.result_hooks = []
        # self.connect(self.result_handle)

    def run_result_hooks(self, *args, **kwargs):
        

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
