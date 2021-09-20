# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox
from typing import Callable


class Dialog(QMessageBox):
    def __init__(self, title: str = None, message: str = None, parent=None, hook=None):
        """
        创建一个提示窗

        :param title: 提示窗标题
        :param message: 提示窗需要显示的文本
        """
        super(Dialog, self).__init__(parent)
        self.setWindowTitle(title)
        self.setText(message)
        self.hooks = []
        self.buttonClicked.connect(self.run)

    def add_hook(self, hook: Callable):
        if callable(hook):
            self.hooks.append(hook)

    def run(self, btn):
        for hook in self.hooks:
            hook()


class InfoDialog(Dialog):
    def __init__(self, title: str = '提示', text: str = None, infomativeText: str = None, parent=None):
        super(InfoDialog, self).__init__(title=title, parent=parent, message=text)
        self.setInformativeText(infomativeText)
        self.setIcon(QMessageBox.Information)

        # 设置标准按钮
        self.setStandardButtons(QMessageBox.Ok)

        # 设置默认按钮
        self.setDefaultButton(QMessageBox.Ok)

        # 退出按钮(按下键盘Esc键时激活的按钮)
        self.setEscapeButton(QMessageBox.Ok)


class QuestionDialog(Dialog):
    def __init__(self, title: str = 'Question', text: str = None, infomativeText: str = None, parent=None):
        super(QuestionDialog, self).__init__(title=title, message=text, parent=parent)
        self.setInformativeText(infomativeText)
        self.setIcon(QMessageBox.Question)

        # 设置标准按钮
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # 设置默认按钮
        self.setDefaultButton(QMessageBox.Yes)

        # 退出按钮
        self.setEscapeButton(QMessageBox.No)

        self.yesRoleHook = []
        self.NoRoleHook = []

    def add_yesRole_hook(self, hook: Callable):
        if callable(hook):
            self.yesRoleHook.append(hook)

    def add_noRole_hook(self, hook: Callable):
        if callable(hook):
            self.NoRoleHook.append(hook)

    def run_yesRole_hook(self):
        for hook in self.yesRoleHook:
            hook()

    def run_noRole_hook(self):
        for hook in self.NoRoleHook:
            hook()

    def run(self, btn):
        role = self.buttonRole(btn)
        if role == QMessageBox.YesRole:
            self.run_yesRole_hook()
        elif role == QMessageBox.NoRole:
            self.run_noRole_hook()