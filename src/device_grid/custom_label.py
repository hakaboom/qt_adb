# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from src.button import CustomButton


class TitleLabel(QWidget):
    def __init__(self, title: str, text: str = 'None', parent=None):
        """
        初始化

        Args:
            title: 标题
            text: 需要输入的内容

        Returns:
            None
        """
        super(TitleLabel, self).__init__(parent)
        self.title = QLabel(title, self)
        self.text = QLabel(text, self)

        self.mainLayout = QGridLayout(self)
        self.mainLayout.addWidget(self.title, 0, 0)
        self.mainLayout.addWidget(self.text, 0, 1, 1, 2)

    def setText(self, text: str):
        self.text.setText(text)

    def setTitle(self, text: str):
        self.title.setText(text)


class DropQLine(QLineEdit):
    def __init__(self, text: str = None, placeholderText: str = None, parent=None):
        super(DropQLine, self).__init__(text, parent)
        self.setAcceptDrops(True)
        self.setPlaceholderText(placeholderText)

    def dragEnterEvent(self, e):
        if e.mimeData().text().endswith('.srt'):  # 如果是.srt结尾的路径接受
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):  # 放下文件后的动作
        path = e.mimeData().text().replace('file:///', '')  # 删除多余开头
        self.setText(path)


class FileChoseLineEdit(QWidget):
    def __init__(self, title: str, text: str = None, placeholderText: str = None, btn_text: str = None, parent=None):
        super(FileChoseLineEdit, self).__init__(parent)

        self.setAcceptDrops(True)
        self.title = QLabel(title, self)
        self.text = DropQLine(text, placeholderText, parent=self)

        self.chose_btn = CustomButton(text=btn_text)

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.addWidget(self.title)
        self.mainLayout.addWidget(self.text)
        self.mainLayout.addWidget(self.chose_btn)

    def set_btn_hook(self, hook):
        self.chose_btn.set_click_hook(hook)

    def setText(self, text: str):
        self.text.setText(text)

    def setTitle(self, text: str):
        self.title.setText(text)
    #
    # def file_dialog(self):
    #     m = QFileDialog.getOpenFileNames()
    #     if m and m[0]:
    #         self.setText(m[0][0])
