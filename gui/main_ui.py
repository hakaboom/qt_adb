# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from adbutils import ADBDevice


from src.device_group import deviceInfoWidget, deviceToolWidget
from src.button import CustomButton
from src.fold_widget import foldWidget
from gui.thread import Thread


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        self.selected_device = None  # type: ADBDevice
        self.devices_list = []

        self.resize(960, 540)
        self.setFont(QFont("Microsoft YaHei"))
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)

        self.setCentralWidget(self.main_widget)
        # ----------------------设置窗口标题----------------------
        self.setWindowTitle("test")  # 设置窗口名
        # ----------------------设备栏----------------------
        self.devices_chose_list = foldWidget()  # type: foldWidget
        self.init_devices_list()  # 初始化device_list
        self.main_layout.addWidget(self.devices_chose_list)
        # ----------------------设备功能栏----------------------
        self.device_widget = QWidget(objectName='device_tool_widget')
        # device_widget设置为水平布局
        self.device_layout = QHBoxLayout(self.device_widget)
        self.device_layout.setObjectName('deviceLayout')
        self.device_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        # device_widget添加到主布局
        self.main_layout.addWidget(self.device_widget)
        # ----------------设备信息_常用操作界面-----------------
        # 将设备信息界与设备常用功能界面,放置在一个水平布局中.
        self.device_info_tool_widget = QWidget(objectName='deviceInfoAndToolWidegt')
        # self.device_info_tool_widget.setStyleSheet('background-color: rgb(85, 170, 0);')
        self.device_info_tool_layout = QHBoxLayout(self.device_info_tool_widget)
        self.device_info_tool_layout.setObjectName('deviceInfoAndToolLayout')
        self.device_info_tool_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.device_layout.addWidget(self.device_info_tool_widget)
        # ----------------------设备信息界面----------------------
        self.device_info_widget = deviceInfoWidget()  # type: deviceInfoWidget
        self.device_info_widget.setObjectName('deviceInfoWidget')
        self.device_info_tool_layout.addWidget(self.device_info_widget)
        self.device_info_widget.setMinimumSize(QSize(220, 300))
        self.device_info_widget.setMaximumSize(QSize(220, 300))
        self.init_update_device_info_hook()
        # ----------------------常用工具界面----------------------
        self.device_tool_widget = deviceToolWidget()
        self.device_info_tool_layout.addWidget(self.device_tool_widget)
        self.device_tool_widget.setMinimumSize(QSize(400, 300))
        self.device_tool_widget.setMaximumSize(QSize(400, 300))

        # ----------------------主界面---------------------------
        # 设置回调函数
        self.init_devices_chose_list_btn_hook()

    def init_devices_list(self):
        devices = ADBDevice().devices
        if devices:
            for device, state in devices.items():
                if state == 'device':
                    item = QListWidgetItem(self.devices_chose_list)
                    button = CustomButton(text=device)
                    button.device = ADBDevice(device_id=device)

                    self.devices_chose_list.add_button(item, button)
                    self.devices_list.append(button.device)

    def init_devices_chose_list_btn_hook(self):
        """
        设置点击设备时的回调函数
        设置selected_device为当前按钮
        """
        btn_list = self.devices_chose_list.get_button_list()
        for btn in btn_list:
            def hook(cls):
                adb = btn.device  # type: ADBDevice

                def fun():
                    # 根据adb设备更新设备信息
                    cls.selected_device = adb
                    cls.device_info_widget.update_thread.start()

                return fun
            btn.set_click_hook(hook=hook(self))

        # 默认第一个为启动状态
        if btn_list:
            btn_list[0].run_hook()

    def init_update_device_info_hook(self):
        def callback():

            def fun():
                device = self.selected_device
                print(f'更新设备信息, device={device}, id={device.device_id}')
                displayInfo = device.displayInfo
                width, height = displayInfo['width'], displayInfo['height']
                return {
                    'serialno': device.device_id,
                    'model': device.model,
                    'manufacturer': device.manufacturer,
                    'memory': device.memory,
                    'displaySize': f'{width}x{height}',
                    'android_version': device.abi_version,
                    'sdk_version': device.sdk_version,
                }

            return fun

        self.device_info_widget.update_thread.set_hook(callback())



