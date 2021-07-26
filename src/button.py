# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize


class CustomButton(QPushButton):
    # 按钮作为开关

    def __init__(self, item, hook=None, *args, **kwargs):
        super(CustomButton, self).__init__(*args, **kwargs)
        self.item = item
        self.onClick_fun = hook
        self.clicked.connect(self.onClick_button)
        # self.setCheckable(True)  # 设置可选中

    def resizeEvent(self, event):
        # 解决item的高度问题
        super(CustomButton, self).resizeEvent(event)
        self.item.setSizeHint(QSize(self.minimumWidth(), self.height()))

    def set_onClick_fun(self, hook):
        self.onClick_fun = hook

    def onClick_button(self):
        if callable(self.onClick_fun):
            self.onClick_fun()
