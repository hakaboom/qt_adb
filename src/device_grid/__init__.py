# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from .custom_label import TitleLabel
from adbutils import ADBDevice, ADBClient
from loguru import logger
import time


class deviceGrid(QWidget):
    def __init__(self, parent=None):
        super(deviceGrid, self).__init__(parent)

        self.setMinimumWidth(640)
        self.setMaximumWidth(640)
        self.mainLayout = QGridLayout(self)
        self.platform = TitleLabel('平台：')
        self.serialno = TitleLabel('序列号：')
        self.memory = TitleLabel('内存容量：')
        self.storage = TitleLabel('储存容量：')
        self.displaySize = TitleLabel('分辨率：')
        self.dpi = TitleLabel('dpi：')
        self.version = TitleLabel('系统版本：')

        self.mainLayout.addWidget(self.platform, 0, 0)
        self.mainLayout.addWidget(self.serialno, 0, 1)
        self.mainLayout.addWidget(self.memory, 0, 2)
        self.mainLayout.addWidget(self.storage, 0, 3)
        self.mainLayout.addWidget(self.displaySize, 1, 0)
        self.mainLayout.addWidget(self.dpi, 1, 1)
        self.mainLayout.addWidget(self.version, 1, 2)

    def update_label(self, title, value):
        if hasattr(self, title):
            label = getattr(self, title)  # type: TitleLabel
            label.setText(value)

    def update_label_from_device(self, device):
        if isinstance(device, ADBDevice):
            """ 设备为android """
            self.update_label('platform', '安卓')
            self.update_label('serialno', 'test')
            self.update_label('memory', device.memory)
            self.update_label('storage', '128G')

            displayInfo = device.displayInfo
            width = displayInfo['width']
            height = displayInfo['height']
            self.update_label('displaySize', f'{width}x{height}')
            self.update_label('dpi', device.getprop('ro.sf.lcd_density'))  # TODO: ADB接口增加dpi
