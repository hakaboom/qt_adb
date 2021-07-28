# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from src.custom_label import TitleLabel, DropQLineEdit, FileDropLineEdit
from adbutils import ADBDevice


class deviceInfoWidget(QGroupBox):
    def __init__(self, parent=None):
        super(deviceInfoWidget, self).__init__('设备信息', parent)

        self.main_layout = QFormLayout(self)
        self.main_layout.setFormAlignment(Qt.AlignVCenter)
        self.main_layout.setVerticalSpacing(15)

        loading_tips = '读取中...'
        self.serialno = TitleLabel('设备名：', loading_tips)
        self.model = TitleLabel('手机型号：', loading_tips)
        self.manufacturer = TitleLabel('手机厂商：', loading_tips)
        self.memory = TitleLabel('内存容量：', loading_tips)
        self.displaySize = TitleLabel('分辨率：', loading_tips)
        self.android_version = TitleLabel('安卓版本：', loading_tips)
        self.sdk_version = TitleLabel('SDK版本：', loading_tips)

        self.main_layout.addRow(self.serialno.title, self.serialno.text)
        self.main_layout.addRow(self.model.title, self.model.text)
        self.main_layout.addRow(self.manufacturer.title, self.manufacturer.text)
        self.main_layout.addRow(self.memory.title, self.memory.text)
        self.main_layout.addRow(self.displaySize.title, self.displaySize.text)
        self.main_layout.addRow(self.android_version.title, self.android_version.text)
        self.main_layout.addRow(self.sdk_version.title, self.sdk_version.text)

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


class deviceToolWidget(QGroupBox):
    def __init__(self, parent=None):
        super(deviceToolWidget, self).__init__('常用工具', parent)

        self.main_layout = QFormLayout(self)
        self.main_layout.setFormAlignment(Qt.AlignVCenter)

        self.install_app = FileDropLineEdit('安装应用', placeholderText='拖入需要安装的APK文件', btn_text='开始安装',
                                            extension=('.apk',))
        self.uninstall_app = 1

        self.main_layout.addRow(self.test)
