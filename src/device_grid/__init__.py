# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from .custom_label import TitleLabel
from loguru import logger


class deviceGrid(QWidget):
    def __init__(self, parent=None):
        super(deviceGrid, self).__init__(parent)

        self.mainLayout = QGridLayout(self)

        self.platform = TitleLabel('平台：', '安卓')
        self.serialno = TitleLabel('序列号：')
        self.memory = TitleLabel('内存容量：')
        self.storage = TitleLabel('储存容量：')
        self.displaySize = TitleLabel('分辨率：')
        