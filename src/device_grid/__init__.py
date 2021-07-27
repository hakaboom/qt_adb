# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from .custom_label import TitleLabel
from adbutils import ADBDevice, ADBClient
from loguru import logger
import time


class deviceInfoWidget(QGroupBox):
    def __init__(self, parent=None):
        super(deviceInfoWidget, self).__init__('设备信息', parent)
        self.setMinimumSize(QSize(220, 260))
        self.setMaximumSize(QSize(220, 260))

        self.mainLayout = QFormLayout(self)
        self.mainLayout.setFormAlignment(Qt.AlignVCenter)
        self.mainLayout.setVerticalSpacing(20)

        self.serialno = TitleLabel('设备名：', '读取中')
        self.model = TitleLabel('手机型号：', '读取中')
        self.manufacturer = TitleLabel('手机厂商：', '读取中')
        self.memory = TitleLabel('内存容量：', '读取中')
        self.displaySize = TitleLabel('分辨率：', '读取中')
        self.android_version = TitleLabel('安卓版本：', '读取中')
        self.sdk_version = TitleLabel('SDK版本：', '读取中')

        self.mainLayout.addRow(self.serialno.title, self.serialno.text)
        self.mainLayout.addRow(self.model.title, self.model.text)
        self.mainLayout.addRow(self.manufacturer.title, self.manufacturer.text)
        self.mainLayout.addRow(self.memory.title, self.memory.text)
        self.mainLayout.addRow(self.displaySize.title, self.displaySize.text)
        self.mainLayout.addRow(self.android_version.title, self.android_version.text)
        self.mainLayout.addRow(self.sdk_version.title, self.sdk_version.text)

    def update_label(self, title, value):
        if hasattr(self, title):
            label = getattr(self, title)  # type: TitleLabel
            label.setText(str(value))

    def update_label_from_device(self, device: ADBDevice):
        if isinstance(device, ADBDevice):
            displayInfo = device.displayInfo
            width, height = displayInfo['width'], displayInfo['height']

            self.update_label('serialno', device.device_id)
            self.update_label('model', device.model)
            self.update_label('manufacturer', device.manufacturer)
            self.update_label('memory', device.memory)
            self.update_label('displaySize', f'{width}x{height}')
            self.update_label('android_version', device.abi_version)
            self.update_label('sdk_version', device.sdk_version)


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
