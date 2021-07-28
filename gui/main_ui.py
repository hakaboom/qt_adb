# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtWidgets import *
from adbutils import ADBDevice


from src.device_grid import deviceGrid, deviceInfoWidget
from src.device_grid.custom_label import FileChoseLineEdit
from src.button import CustomButton
from src.fold_widget import foldWidget
import sys
import json
import os
from loguru import logger


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        self.selected_device = None

        self.resize(960, 540)
        self.setFont(QFont("Microsoft YaHei"))
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)

        self.setCentralWidget(self.main_widget)
        # ----------------------设置窗口标题----------------------
        self.setWindowTitle("test")  # 设置窗口名
        # ----------------------设备栏----------------------
        self.devices_list = foldWidget()  # type: foldWidget
        self.init_devices_list()  # 初始化device_list
        self.main_layout.addWidget(self.devices_list)
        # ----------------------设备功能栏----------------------
        self.device_widget = QWidget(objectName='devices_tools_widget')
        self.device_layout = QVBoxLayout(self.device_widget, objectName='devices_tools_layout')
        self.main_layout.addWidget(self.device_widget)
        # ----------------------设备信息栏----------------------
        self.device_info_widget = deviceInfoWidget()  # type: deviceInfoWidget
        # ==self.device_info_widget.setStyleSheet('background-color: rgb(85, 170, 0);')
        self.device_layout.addWidget(self.device_info_widget)

        # ----------------------设备功能栏----------------------
        self.device_layout.addStretch(0)
        # ----------------------主界面----------------------
        # 设置回调函数
        self.device_btn_hook()

    def init_devices_list(self):
        devices = ADBDevice().devices
        if devices:
            for device, state in devices.items():
                if state == 'device':
                    item = QListWidgetItem(self.devices_list)
                    button = CustomButton(text=device)
                    button.device = ADBDevice(device_id=device)
                    self.devices_list.add_button(item, button)

    def device_btn_hook(self):
        btn_list = self.devices_list.get_button_list()
        for btn in btn_list:
            def hook(cls):
                adb = btn.device  # type: ADBDevice

                def fun():
                    # 根据adb设备更新设备信息
                    cls.device_info_widget.update_label_from_device(adb)
                return fun
            btn.set_click_hook(hook=hook(self))

        # 默认第一个为启动状态
        if btn_list:
            btn_list[0].run_hook()








