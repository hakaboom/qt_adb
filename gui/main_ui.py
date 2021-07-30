# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from adbutils import ADBDevice
from adbutils.exceptions import AdbBaseError, AdbInstallError


from src.device_group import deviceInfoWidget, deviceToolWidget
from src.button import CustomButton
from src.fold_widget import foldWidget
from gui.thread import Thread, LoopThread
from src.custom_dialog import InfoDialog

import time


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        self.resize(960, 540)
        self.setFont(QFont("Microsoft YaHei"))
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)

        self.setCentralWidget(self.main_widget)
        # ----------------------设置窗口标题----------------------
        self.setWindowTitle("test")  # 设置窗口名
        # ----------------------设备栏----------------------
        self.devices_chose_list = foldWidget()  # type: foldWidget
        # self.init_devices_list()  # 初始化device_list
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

        # ----------------------常用工具界面----------------------
        self.device_tool_widget = deviceToolWidget()
        self.device_info_tool_layout.addWidget(self.device_tool_widget)
        self.device_tool_widget.setMinimumSize(QSize(400, 300))
        self.device_tool_widget.setMaximumSize(QSize(400, 300))

        # ----------------------主界面---------------------------
        self.selected_device = None
        self.devices_list = []
        # 设置回调函数
        self.devices_list_thread = None
        self.device_info_thread = None
        self.init_devices_list_loop()
        self.init_install_app_hook()
        self.init_device_info_hook()

    def init_devices_list_loop(self):
        def callback():
            def fun():
                while True:
                    devices = ADBDevice().devices
                    if devices:
                        return devices
            return fun

        self.devices_list_thread = LoopThread(hook=callback(), delay=2)
        self.devices_list_thread.connect(self.update_devices_list)
        self.devices_list_thread.start()

    def update_devices_list(self, deviceList):
        deviceList = list(filter(None, [state == 'device' and (device_id, state) or None
                                        for device_id, state in deviceList.items()]))
        deviceList.sort()
        # TODO: 还需要考虑设备断开连接的状态
        for device_id, state in deviceList:
            if state == 'device' and device_id not in self.devices_list:
                item = QListWidgetItem(self.devices_chose_list)
                button = CustomButton(text=device_id)
                button.device = ADBDevice(device_id=device_id)

                self.devices_chose_list.add_button(item, button)
                def callback(cls):
                    adb = button.device
                    def fun():
                        print(f'点击设备：{adb.device_id}')
                        cls.selected_device = adb

                    return fun
                button.set_click_hook(callback(cls=self))
                self.devices_list.append(device_id)

    def init_device_info_hook(self):
        def callback(cls):
            def fun():
                while True:
                    device = cls.selected_device
                    if not device:
                        return None
                    displayInfo = device.displayInfo
                    width, height = displayInfo['width'], displayInfo['height']
                    print(f'更新设备信息, device={device}, id={device.device_id}')

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

        self.device_info_thread = LoopThread(hook=callback(cls=self), delay=2)
        self.device_info_thread.connect(self.device_info_widget.update_label)
        self.device_info_thread.start()

    def init_install_app_hook(self):
        install_widget = self.device_tool_widget.install_app
        install_widget.update_thread = Thread()

        def callback(cls):
            def fun():
                device = cls.selected_device  # type: ADBDevice
                path = cls.get_install_app_path()
                print(f"安装应用={path or None}")
                if path:
                    install_widget.setEnabled(False)
                    try:
                        device.install(local=path)
                    except Exception as e:
                        return AdbInstallError(f'应用安装失败\n{e}')
                    finally:
                        install_widget.setEnabled(True)
            return fun

        install_widget.update_thread.set_hook(callback(cls=self))
        install_widget.set_btn_hook(install_widget.update_thread.start)
        install_widget.update_thread.connect(self.raise_dialog)

    def get_install_app_path(self):
        """ 从控件中获取安装应用的路径 """
        path = self.device_tool_widget.install_app.getText()
        return path

    def raise_dialog(self, exceptions):
        if isinstance(exceptions, AdbBaseError):
            dialog = InfoDialog(text='错误', infomativeText=str(exceptions), parent=self)
            dialog.open()
