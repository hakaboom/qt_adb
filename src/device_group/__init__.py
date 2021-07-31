# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from src.custom_label import TitleLabel, DropQLineEdit, FileDropLineEdit, TitleComboLineEdit
from adbutils import ADBDevice
from gui.thread import Thread


class deviceInfoWidget(QGroupBox):
    def __init__(self, parent=None):
        super(deviceInfoWidget, self).__init__('设备信息', parent)

        self.main_layout = QFormLayout(self)
        self.main_layout.setFormAlignment(Qt.AlignVCenter)
        self.main_layout.setVerticalSpacing(16)

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


class deviceToolWidget(QGroupBox):
    def __init__(self, parent=None):
        super(deviceToolWidget, self).__init__('常用工具', parent)

        self.main_layout = QFormLayout(self)
        self.main_layout.setFormAlignment(Qt.AlignVCenter)

        self.install_app = FileDropLineEdit('安装应用:', placeholderText='拖入需要安装的APK文件', btn_text='开始安装',
                                            extension=('.apk',))
        self.uninstall_app = TitleComboLineEdit(title='卸载应用:', items=['1', '2', '3', '4'], btn_text='开始卸载')
        self.clear_app = TitleComboLineEdit(title='清除数据:', btn_text='开始清除')

        self.main_layout.addRow(self.install_app)
        self.main_layout.addRow(self.uninstall_app)
        self.main_layout.addRow(self.clear_app)
