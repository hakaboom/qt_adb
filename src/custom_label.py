# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from src.button import CustomButton


class TitleLabel(QWidget):
    def __init__(self, title: str, text: str = None, parent=None):
        """
        带标题的文本控件,例如 用户名：xxxxxxxx

        :param title: 标题
        :param text: 需要输入的内容
        :param parent: 父控件
        """
        super(TitleLabel, self).__init__(parent)
        self.title = QLabel(title, self)
        self.text = QLabel(text, self)

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.addWidget(self.title)
        self.mainLayout.addWidget(self.text)

    def setText(self, text: str):
        self.text.setText(text)
        return self

    def setTitle(self, text: str):
        self.title.setText(text)
        return self


class TitleLineEdit(QWidget):
    def __init__(self, title: str, text: str = None, placeholderText: str = None, parent=None):
        """
        带有标题的输入控件

        :param title: 需要输入的标题
        :param text: 默认的文本
        :param placeholderText: 提示文本
        :param parent: 父控件
        """
        super(TitleLineEdit, self).__init__(parent)
        self.title = QLabel(title, parent=self)
        self.lineEdit = QLineEdit(text)
        if placeholderText:
            self.lineEdit.setPlaceholderText(placeholderText)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.lineEdit)

    def setTitle(self, text: str):
        """ 设置标题文本 """
        self.title.setText(text)
        return self

    def setText(self, text: str):
        """ 设置输入框文本内容 """
        self.lineEdit.setText(text)
        return self

    def getText(self):
        """ 获取输入框内文本内容 """
        return self.lineEdit.text()

    def set_lineEdit_enable(self, flag: bool):
        """ 设置输入框 True:允许写入/False:无法写入"""
        self.lineEdit.setEnabled(flag)
        return self


class FileDropLineEdit(QWidget):
    def __init__(self, title: str, text: str = None, placeholderText: str = None, btn_text: str = None,
                 extension: tuple = None, parent=None):
        """
        带有标题、拖入功能输入框、按钮的组合控件

        :param title: 标题文本
        :param text: 输入框默认文本
        :param placeholderText: 输入框提示文本
        :param btn_text: 按钮文本
        :param extension: 输入框拖入文件后缀名筛选
        :param parent: 后缀名
        """
        super(FileDropLineEdit, self).__init__(parent)

        self.title = QLabel(title)
        self.lineEdit = DropQLineEdit(text, placeholderText, extension)

        self.chose_btn = CustomButton(text=btn_text)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.lineEdit)
        self.main_layout.addWidget(self.chose_btn)

    def set_btn_hook(self, hook):
        """ 设置按钮回调函数 """
        self.chose_btn.set_click_hook(hook)

    def getText(self):
        """ 获取输入框内文本"""
        return self.lineEdit.text()

    def setText(self, text: str):
        """ 设置输入框文本 """
        self.lineEdit.setText(text)

    def setTitle(self, text: str):
        """ 获取标题文本 """
        self.title.setText(text)


class DropQLineEdit(QLineEdit):
    def __init__(self, text: str = None, placeholderText: str = None, extension: tuple = None, parent=None):
        """
        拖拽文件到文本框内

        :param text: 默认的文本
        :param placeholderText: 提示文本
        :param extension: 拖入文件后缀名筛选
        :param parent: 父控件
        """
        super(DropQLineEdit, self).__init__(text, parent)
        self.extension = extension
        self.setAcceptDrops(True)
        self.setPlaceholderText(placeholderText)

    def dragEnterEvent(self, e):
        if e.mimeData().text().endswith(self.extension):  # 如果是.srt结尾的路径接受
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):  # 放下文件后的动作
        path = e.mimeData().text().replace('file:///', '')  # 删除多余开头
        self.setText(path)
