# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox


class Dialog(QMessageBox):
    def __init__(self, title: str = None, message: str = None, parent=None):
        """
        创建一个提示窗

        :param title: 提示窗标题
        :param message: 提示窗需要显示的文本
        """
        super(Dialog, self).__init__(parent)
        self.setWindowTitle(title)
        self.setText(message)


class InfoDialog(Dialog):
    def __init__(self, text: str = None, infomativeText: str = None, parent=None):
        super(InfoDialog, self).__init__(title='Info', parent=parent)
        self.setText(text)
        self.setInformativeText(infomativeText)
