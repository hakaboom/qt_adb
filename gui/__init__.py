# -*- coding: utf-8 -*-
import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, QPoint, QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from adbutils import ADBDevice, ADBClient
from adbutils.exceptions import AdbBaseError, AdbInstallError
from loguru import logger


from src import BaseControl, ComboBoxWithButton, GroupBox, Label
from gui.thread import Thread, LoopThread
from src.custom_dialog import InfoDialog

from typing import Union, Tuple, List


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        self.resize(QSize(960, 540))
        self.setFixedSize(self.width(), self.height())
        self.setFont(QFont("Microsoft YaHei"))

        # mian_widget 布局: 水平布局
        self.main_widget = QWidget(objectName='main_widget')
        self.main_layout = QHBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("test")

        # 功能栏 布局: 无
        self.function_bar = QWidget(objectName='function_bar')
        # self.function_bar.setStyleSheet('background-color: rgb(0, 170, 255);')
        self.main_layout.addWidget(self.function_bar)

        # 设备区域 布局: 水平布局
        self.device_main = QWidget(objectName='device_main')
        self.main_layout.addWidget(self.device_main)
        # self.device_main.setStyleSheet('background-color: rgb(170, 255, 0);')
        self.device_main_layout = QHBoxLayout(self.device_main)
        self.device_main_layout.setObjectName('device_main_layout')

        self.main_layout.setStretch(0, 2)
        self.main_layout.setStretch(1, 9)

        # 设备区域控件 布局: 垂直布局
        self.device_config_widget = QWidget(objectName='device_config')
        # self.device_config_widget.setStyleSheet('background-color: rgb(255, 170, 0);')
        self.device_main_layout.addWidget(self.device_config_widget)
        self.device_main_layout.setContentsMargins(5, 5, 5, 5)

        self.device_tool_widget = QWidget(objectName='device_tool')
        # self.device_tool_widget.setStyleSheet('background-color: rgb(0, 255, 255);')
        self.device_main_layout.addWidget(self.device_tool_widget)

        self.device_main_layout.setStretch(0, 3)
        self.device_main_layout.setStretch(1, 8)

        self.device_config_layout = QVBoxLayout(self.device_config_widget)
        self.device_config_layout.setContentsMargins(5, 5, 5, 5)

        # --------------------------------------------------------------------------------------------------------------
        # 设备选择控件 布局: 垂直布局
        self.device_chose_control = BaseControl(title='设备选择', objectName='device_chose_control')
        self.device_chose_control.widget.setStyleSheet('background-color: rgb(255, 255, 127);')
        self.device_chose = ComboBoxWithButton(parent=self.device_chose_control.widget, btn_text='刷新设备')
        self.device_chose.comboBox.setMinimumHeight(30)
        self.device_chose.btn.setMinimumHeight(30)
        self.device_chose_thread = None
        self._set_device_chose_callback()
        # --------------------------------------------------------------------------------------------------------------
        self.device_info_control = BaseControl(title='设备信息', objectName='device_info_control')
        self.device_info_control.setStyleSheet('background-color: rgb(255, 170, 0);')
        self._create_device_info_widget()
        self._set_device_info_callback()

        self.device_config_layout.addWidget(self.device_chose_control)
        self.device_config_layout.addWidget(self.device_info_control)

        self.device_config_layout.setStretch(0, 1)
        self.device_config_layout.setStretch(1, 6)

    def _set_device_chose_callback(self):
        """ 使用device_chose控件进行回调 """
        # 使用控件self.device_chose,绑定btn回调,像comboBox中刷新组件
        client = ADBClient()

        def callback(adb: ADBClient, cls):
            def fun():
                logger.debug('刷新设备')
                cls.device_chose.setEnabled(False)

                current_device = cls.device_chose.currentText()
                # step1: 清除所有item
                cls.device_chose.clear()

                # step2: 讲选中设备,重新添加进item
                if current_device:
                    cls.device_chose.addItem(current_device)

                # 从adb devices中,获取最新的设备信息
                devices = adb.devices
                for device_id, state in devices.items():
                    if state != 'device' or device_id == current_device:
                        continue
                    cls.device_chose.addItem(device_id)

                cls.device_chose.setEnabled(True)
                logger.debug(devices)

            return fun

        update_thread = Thread()
        update_thread.set_hook(callback(adb=client, cls=self))

        self.device_chose.btn.update_thread = update_thread
        self.device_chose.btn.set_click_hook(update_thread.start)

    def _create_device_info_widget(self):

        groupBox = GroupBox(parent=self.device_info_control.widget)
        groupBox.main_layout.setVerticalSpacing(15)

        loading_tips = '读取中...'
        groupBox.serialno = Label(loading_tips)
        groupBox.model = Label(loading_tips)
        groupBox.manufacturer = Label(loading_tips)
        groupBox.memory = Label(loading_tips)
        groupBox.displaySize = Label(loading_tips)
        groupBox.android_version = Label(loading_tips)
        groupBox.sdk_version = Label(loading_tips)

        groupBox.addRow('设备标识:', groupBox.serialno)
        groupBox.addRow('手机型号:', groupBox.model)
        groupBox.addRow('手机厂商:', groupBox.manufacturer)
        groupBox.addRow('内存容量:', groupBox.memory)
        groupBox.addRow('分辨率:', groupBox.displaySize)
        groupBox.addRow('安卓版本:', groupBox.android_version)
        groupBox.addRow('SDK版本:', groupBox.sdk_version)

    @staticmethod
    def _get_device_info(device: ADBDevice):
        displayInfo = device.getPhysicalDisplayInfo()
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

    def _set_device_info_callback(self):
        def callback(cls):
            def fun():
                logger.warning('test')
                time.sleep(5)
                current_device = cls.device_chose.currentText()
                logger.debug(f'tasdasd:{current_device}')

            return fun

        update_thread = Thread()
        update_thread.set_hook(callback(cls=self))

        self.device_chose.activated.connect(update_thread.test)
