# -*- coding: utf-8 -*-
from PyQt5.Qt import (QApplication, QWidget, QPushButton,
                      QThread, QMutex, pyqtSignal)
from src.custom_dialog import InfoDialog
import sys
import time
from functools import wraps
from typing import Tuple, Type, Callable
from loguru import logger


class Thread(QThread):
    _signal = pyqtSignal(object)

    def __init__(self, exceptions: Tuple[Type[Exception], ...] = (Exception,)):
        """
        创建新线程
        """
        super(Thread, self).__init__()
        self.hooks = []
        self.exceptions = exceptions  # [Exception, AdbBaseError]
        self.exceptions_hook = {}
        self.exceptions_hook_run()

    def exceptions_hook_run(self):
        """
        运行异常hook

        Returns:
            None
        """
        def run(*args, **kwargs):
            # 处理信号槽返回值,只有args的第一参数为exception时,才会运行
            if args and isinstance(args[0], Exception):
                exception = args[0]
                if type(exception) in self.exceptions_hook.keys():
                    for hook in self.exceptions_hook.get(type(exception)):
                        hook(exception)
                else:
                    for _exceptions, hooks in self.exceptions_hook.items():
                        if isinstance(exception, _exceptions):
                            for hook in self.exceptions_hook.get(_exceptions):
                                hook(exception)

        self.connect(run)

    def add_exception_hook(self, exception: Type[Exception], hook: Callable):
        """
        添加异常hook

        Args:
            exception: 需要添加的异常
            hook: hook函数

        Returns:
            None
        """
        if issubclass(exception, Exception) and isinstance(hook, Callable):
            if exception not in self.exceptions_hook.keys():
                self.exceptions_hook[exception] = []
            self.exceptions_hook[exception].append(hook)

    def add_hook(self, hook):
        """
        进程会运行的函数

        Args:
            hook: 需要运行的函数

        Returns:
            None
        """
        def safe_function():
            def func():
                try:
                    return hook()
                except self.exceptions as err:
                    return err
            return func

        self.hooks.append(safe_function())

    def connect(self, func):
        self._signal.connect(func)

    def run(self):
        ret = None
        for hook in self.hooks:
            if callable(hook):
                ret = hook()
            if ret:
                self._signal.emit(ret)


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

