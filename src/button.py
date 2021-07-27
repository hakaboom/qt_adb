# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from inspect import isfunction


class CustomButton(QPushButton):
    # 按钮作为开关
    def __init__(self, text: str = None, item=None, hook=None, icon=None, parent=None):
        param = [icon, text, parent]
        super(CustomButton, self).__init__(*list(filter(None, param)))
        self.item = item
        self.hook = hook
        self.clicked.connect(self.run_hook)

    def resizeEvent(self, event):
        # 解决item的高度问题
        super(CustomButton, self).resizeEvent(event)
        if self.item:
            self.item.setSizeHint(QSize(self.minimumWidth(), self.height()))

    def set_click_hook(self, hook):
        self.hook = hook

    def run_hook(self):
        if callable(self.hook):
            return self.hook()
