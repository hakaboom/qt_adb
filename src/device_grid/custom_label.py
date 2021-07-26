# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *


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

        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.title, 0, 0)
        mainLayout.addWidget(self.text, 0, 1, 1, 2)

    def setText(self, text: str):
        self.text.setText(text)

    def setTitle(self, text: str):
        self.title.setText(text)