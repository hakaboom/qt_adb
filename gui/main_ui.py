# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from adbutils import ADBDevice

from src.button import CustomButton
from src.fold_widget import foldWidget
import sys
import json
import os
from loguru import logger


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        self.resize(960, 540)
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)
        # ----------------------设置窗口标题----------------------
        self.setWindowTitle("test")  # 设置窗口名

        # ----------------------设备栏----------------------
        self.devices_list = None  # type: foldWidget
        self.devices_list_widget = QWidget()
        self.devices_list_widget.setObjectName('devices_list_widget')
        self.devices_list_layout = QVBoxLayout()
        self.devices_list_layout.setObjectName('devices_list_layout')

        self.init_devices_list()  # 初始化device_list

        self.main_layout.addWidget(self.devices_list_widget)
        self.devices_list_layout.addWidget(self.devices_list)
        self.devices_list_widget.setLayout(self.devices_list_layout)
        # ----------------------设备功能栏----------------------
        self.devices_tools_widget = QWidget()
        self.devices_tools_widget.setObjectName('devices_tools_widget')
        self.devices_tools_widget.setStyleSheet('background-color: rgb(85, 170, 0);')
        self.devices_tools_layout = QVBoxLayout()
        self.devices_tools_layout.setObjectName('devices_tools_layout')

        self.main_layout.addWidget(self.devices_tools_widget)
        self.devices_tools_widget.setLayout(self.devices_tools_layout)
        # ----------------------设备信息栏----------------------
        self.devices_info_widget = None  # type: deviceGrid
        self.init_devices_info()
        self.devices_tools_layout.addStretch(0)  # 添加伸缩
        # ----------------------主界面----------------------
        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 100)  # 更改main大小会有影响
        self.main_layout.setSpacing(0)

        # 设置回调函数
        self.device_btn_hook()

    def init_devices_list(self):
        self.devices_list = foldWidget()
        devices = ADBDevice().devices
        if devices:
            for device, state in devices.items():
                item = QListWidgetItem(self.devices_list)
                button = CustomButton(item, text=device, objectName='device_btn')
                button.device = ADBDevice(device_id=device)
                self.devices_list.add_button(item, button)

    def device_btn_hook(self):
        for btn in self.devices_list.get_button_list():
            def hook():
                adb = btn.device  # type: ADBDevice
                def fun():
                    print(adb.displayInfo)
                return fun
            btn.set_onClick_fun(hook())

    def init_devices_info(self):
        """ 配置设置信息 """
        from src.device_grid import deviceGrid
        self.devices_info_widget = deviceGrid()
        self.devices_tools_layout.addWidget(self.devices_info_widget)







