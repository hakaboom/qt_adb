# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox


class Dialog(QMessageBox):
    def __init__(self, title: str = 'Info', message: str = None):
        """
        创建一个提示窗

        :param title: 提示窗标题
        :param message: 提示窗需要显示的文本
        """
        super(Dialog, self).__init__()
        self.message = message
        self.title = title

    def show(self):
        self.open()
