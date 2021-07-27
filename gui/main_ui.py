# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem
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
        self.resize(960, 540)
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)

        self.setCentralWidget(self.main_widget)
        # ----------------------设置窗口标题----------------------
        self.setWindowTitle("test")  # 设置窗口名

        # ----------------------设备栏----------------------
        self.devices_list = foldWidget()  # type: foldWidget
        self.devices_list_layout = QVBoxLayout(self.devices_list, objectName='devices_list_layout')
        self.init_devices_list()  # 初始化device_list
        self.main_layout.addWidget(self.devices_list)
        self.devices_list_layout.addWidget(self.devices_list)
        # ----------------------设备功能栏----------------------
        self.device_widget = QWidget(objectName='devices_tools_widget')
        self.device_layout = QVBoxLayout(self.device_widget, objectName='devices_tools_layout')
        self.main_layout.addWidget(self.device_widget)

        # ----------------------设备信息栏----------------------
        self.device_info_widget = deviceInfoWidget()  # type: deviceInfoWidget
        # ==self.device_info_widget.setStyleSheet('background-color: rgb(85, 170, 0);')
        self.device_layout.addWidget(self.device_info_widget)

        # ----------------------设备功能栏----------------------
        # self.device_tool_widget = QWidget()
        # self.device_tool_height = QVBoxLayout(self.device_tool_widget)
        #
        # self.apk_install = FileChoseLineEdit('安装应用:', placeholderText='请拖入需要安装的APK文件', btn_text='开始安装')
        # self.device_tool_height.addWidget(self.apk_install)
        #
        # self.device_layout.addWidget(self.device_tool_widget)
        self.device_layout.addStretch(0)
        # ----------------------主界面----------------------
        # self.main_layout.setStretch(0, 1)
        # self.main_layout.setStretch(1, 100)  # 更改main大小会有影响
        # self.main_layout.setSpacing(0)

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
            def hook():
                adb = btn.device  # type: ADBDevice
                info_widget = self.device_info_widget

                def fun():
                    info_widget.update_label_from_device(adb)
                return fun
            btn.set_click_hook(hook=hook())

        # 默认第一个为启动状态
        # if btn_list:
        #     btn_list[0].run_hook()








