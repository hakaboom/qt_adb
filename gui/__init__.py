# -*- coding: utf-8 -*-
import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, QPoint, QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from adbutils import ADBDevice, ADBClient
from adbutils.exceptions import AdbBaseError, AdbInstallError
from loguru import logger


from src import BaseControl, ComboBoxWithButton, FormLayout, Label
from src.custom_label import TitleLabel, FileDropLineEdit
from src.device_group import deviceInfoWidget
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
        self.device_tool_widget.setStyleSheet('background-color: rgb(255, 170, 0);')
        self.device_main_layout.addWidget(self.device_tool_widget)

        self.device_main_layout.setStretch(0, 3)
        self.device_main_layout.setStretch(1, 8)

        self.device_config_layout = QVBoxLayout(self.device_config_widget)
        self.device_config_layout.setContentsMargins(5, 5, 5, 5)

        self.device_tool_layout = QVBoxLayout(self.device_tool_widget)
        self.device_tool_layout.setContentsMargins(5, 5, 5, 5)
        # --------------------------------------------------------------------------------------------------------------
        # 设备选择控件 布局: 垂直布局
        self.device_chose_control = BaseControl(title='设备选择', objectName='device_chose_control')
        self.device_chose_widget = self._create_device_chose_widget(parent=self.device_chose_control.widget)
        self.device_chose_thread = None
        self._set_device_chose_callback()
        # --------------------------------------------------------------------------------------------------------------
        # 设备信息控件 布局：垂直布局
        self.device_info_control = BaseControl(title='设备信息', objectName='device_info_control')
        self.device_info_widget = self._create_device_info_widget(parent=self.device_info_control.widget)
        self.device_info_control.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self._set_device_info_callback()

        self.device_config_layout.addWidget(self.device_chose_control)
        self.device_config_layout.addWidget(self.device_info_control)

        self.device_config_layout.setStretch(0, 1)
        self.device_config_layout.setStretch(1, 6)
    # --------------------------------------------------------------------------------------------------------------
        # 应用管理
        self.device_app_control = BaseControl(title='应用管理', objectName='device_app_manager')
        self.device_app_control.widget.setStyleSheet('background-color: rgb(0, 255, 255);')
        self.device_tool_layout.addWidget(self.device_app_control)

        self._create_device_app_widget(parent=self.device_app_control.widget)

    def _set_device_chose_callback(self):
        """ 使用device_chose控件进行回调 """
        # 使用控件self.device_chose_widget,绑定btn回调,像comboBox中刷新组件
        client = ADBClient()

        def callback(adb: ADBClient, cls):
            def fun():
                logger.debug('刷新设备')
                cls.device_chose_widget.setEnabled(False)

                current_device = cls.device_chose_widget.currentText()
                # step1: 清除所有item
                cls.device_chose_widget.clear()

                # step2: 讲选中设备,重新添加进item
                if current_device:
                    cls.device_chose_widget.addItem(current_device)

                try:
                    # 从adb devices中,获取最新的设备信息
                    devices = adb.devices
                    logger.debug(devices)
                    for device_id, state in devices.items():
                        if state != 'device' or device_id == current_device:
                            continue
                        cls.device_chose_widget.addItem(device_id)
                except AdbBaseError as err:
                    return AdbBaseError(err)
                finally:
                    cls.device_chose_widget.setEnabled(True)

            return fun

        update_thread = Thread()
        update_thread.set_hook(callback(adb=client, cls=self))
        update_thread.connect(self.raise_dialog)

        self.device_chose_widget.btn.update_thread = update_thread
        self.device_chose_widget.btn.set_click_hook(update_thread.start)

    @staticmethod
    def _create_device_chose_widget(parent: QWidget):
        widget = ComboBoxWithButton(parent=parent, btn_text='刷新设备')
        widget.comboBox.setMinimumHeight(30)
        widget.btn.setMinimumHeight(30)
        return widget

    @staticmethod
    def _create_device_info_widget(parent: QWidget):
        groupBox = FormLayout(parent=parent)
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

        return groupBox

    @staticmethod
    def _create_device_app_widget(parent: QWidget):
        groupBox = FormLayout(parent=parent)

        groupBox.install = FileDropLineEdit('安装应用:', placeholderText='拖入需要安装的APK文件', btn_text='开始安装',
                                            extension=('.apk',))

        groupBox.addRow(groupBox.install)

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

    def _update_device_info(self, deviceInfo: dict):
        if isinstance(deviceInfo, dict):
            device_info = self.device_info_widget
            device_info.update_label('serialno', deviceInfo['serialno'])
            device_info.update_label('model', deviceInfo['model'])
            device_info.update_label('manufacturer', deviceInfo['manufacturer'])
            device_info.update_label('memory', deviceInfo['memory'])
            device_info.update_label('displaySize', deviceInfo['displaySize'])
            device_info.update_label('android_version', deviceInfo['android_version'])
            device_info.update_label('sdk_version', deviceInfo['sdk_version'])

    def _set_device_info_callback(self):
        def callback(cls):
            def fun():
                cls.device_chose_widget.setEnabled(False)
                try:
                    current_device = cls.device_chose_widget.currentText()
                    device = ADBDevice(current_device)
                    device_info = cls._get_device_info(device)
                    cls._update_device_info(device_info)
                except AdbBaseError as err:
                    return AdbBaseError(err)
                finally:
                    cls.device_chose_widget.setEnabled(True)
            return fun

        update_thread = Thread()
        update_thread.set_hook(callback(cls=self))
        update_thread.connect(self.raise_dialog)

        self.device_chose_widget.currentIndexChanged.connect(lambda: update_thread.start())

    def raise_dialog(self, exceptions):
        if isinstance(exceptions, AdbBaseError):
            logger.error(str(exceptions))
            dialog = InfoDialog(text='错误', infomativeText=str(exceptions), parent=self)
            dialog.open()