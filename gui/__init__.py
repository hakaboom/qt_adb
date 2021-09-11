# -*- coding: utf-8 -*-
import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, QPoint, QRect
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import *
from adbutils import ADBDevice, ADBClient
from adbutils.extra.aapt import Aapt
from adbutils.exceptions import AdbBaseError, AdbInstallError
from baseImage import IMAGE
from loguru import logger


from src import BaseControl, ComboBoxWithButton, FormLayout, Label, cv_to_qtimg
from src.custom_label import TitleLabel, FileDropLineEdit, TitleComboLineEdit
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

        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 9)

        # 设备区域控件 布局: 垂直布局
        self.device_config_widget = QWidget(objectName='device_config')
        # self.device_config_widget.setStyleSheet('background-color: rgb(255, 170, 0);')
        self.device_main_layout.addWidget(self.device_config_widget)
        self.device_main_layout.setContentsMargins(5, 5, 5, 5)

        self.device_tool_widget = QWidget(objectName='device_tool')
        # self.device_tool_widget.setStyleSheet('background-color: rgb(255, 170, 0);')
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
        self.device_app_control = BaseControl(title='应用管理', objectName='device_app_control')
        self.device_tool_layout.addWidget(self.device_app_control)
        self.device_app_info_widget = self._create_device_app_manage_widget(parent=self.device_app_control.widget)
        self._set_app_info_callback()

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
                    return err
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
        widget.btn.setToolTip('点击后刷新设备列表')
        return widget

    @staticmethod
    def _create_device_info_widget(parent: QWidget):
        groupBox = FormLayout(parent=parent)
        groupBox.main_layout.setVerticalSpacing(15)

        loading_tips = '读取中...'

        groupBox.addRow('设备标识:', Label(loading_tips), index='serialno')
        groupBox.addRow('手机型号:', Label(loading_tips), index='model')
        groupBox.addRow('手机厂商:', Label(loading_tips), index='manufacturer')
        groupBox.addRow('内存容量:', Label(loading_tips), index='memory')
        groupBox.addRow('分辨率:', Label(loading_tips), index='displaySize')
        groupBox.addRow('安卓版本:', Label(loading_tips), index='android_version')
        groupBox.addRow('SDK版本:', Label(loading_tips), index='sdk_version')

        return groupBox

    @staticmethod
    def _create_device_app_manage_widget(parent: QWidget):
        # 主控件为self.device_app_control
        """
            控件主布局为垂直布局
            共两个控件icon/info
            icon为水平布局,分别为 app图标--app名
            info为水平布局, 左右两个表单布局,存放app的信息
        """
        main_layout = QVBoxLayout(parent)

        # step1: icon控件
        icon_widget = QWidget(parent)
        icon_widget.setStyleSheet('background-color: rgb(0, 255, 255);')
        icon_layout = QHBoxLayout(icon_widget)

        main_layout.icon = Label()
        image_label = Label(IMAGE('./icon/com.hypergryph.arknights.png'))

        icon_layout.addWidget(image_label)
        icon_layout.addWidget(Label('test'))

        # step2: info控件
        info_widget = QWidget(parent)
        info_widget.setStyleSheet('background-color: rgb(255, 255, 127);')
        info_main_layout = QHBoxLayout(info_widget)
        # 左右布局
        _info_left_widget = QWidget(info_widget)
        _info_right_widget = QWidget(info_widget)
        info_main_layout.addWidget(_info_left_widget)
        info_main_layout.addWidget(_info_right_widget)
        info_left = FormLayout(parent=_info_left_widget)
        info_right = FormLayout(parent=_info_right_widget)

        main_layout.info_left_widget = info_left
        main_layout.info_right_widget = info_right

        info_left.addRow('应用名称：', Label(), index='app_label_name')
        info_left.addRow('应用包名：', Label(), index='app_package_name')
        info_left.addRow('主Activity：', Label(), index='app_main_activity')

        info_right.addRow('版本号：', Label(), index='app_version_id')
        info_right.addRow('版本名：', Label(), index='app_version_name')

        main_layout.addWidget(icon_widget)
        main_layout.addWidget(info_widget)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        return main_layout

    def _set_app_info_callback(self):
        def callback(cls):
            def fun():
                try:
                    device = cls.get_current_device()
                    packageName = device.foreground_package
                    app_info = cls._get_app_info(device=device, packageName=packageName)
                    cls._update_app_info(app_info)
                except AdbBaseError as err:
                    return err
            return fun

        update_thread = Thread()
        update_thread.set_hook(callback(cls=self))
        update_thread.connect(self.raise_dialog)

        self.device_chose_widget.btn.update_thread.set_hook(callback(cls=self))

    @staticmethod
    def _get_app_info(device: ADBDevice, packageName: str):
        aapt = Aapt(device)
        app_info = aapt.get_app_info(packageName=packageName)
        return app_info

    def _update_app_info(self, app_info: dict):
        if isinstance(app_info, dict):
            info_left = self.device_app_info_widget.info_left_widget
            info_right = self.device_app_info_widget.info_right_widget

            info_left.getField('app_label_name').setText(app_info['app_name'])
            info_left.getField('app_package_name').setText(app_info['package_name'])
            info_left.getField('app_main_activity').setText(app_info['launchable_activity'])
            info_right.getField('app_version_id').setText(app_info['versionCode'])
            info_right.getField('app_version_name').setText(app_info['versionName'])

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
            print(device_info.getField('serialno'))
            device_info.getField('serialno').setText(deviceInfo['serialno'])
            device_info.getField('model').setText(deviceInfo['model'])
            device_info.getField('manufacturer').setText(deviceInfo['manufacturer'])
            device_info.getField('memory').setText(deviceInfo['memory'])
            device_info.getField('displaySize').setText(deviceInfo['displaySize'])
            device_info.getField('android_version').setText(deviceInfo['android_version'])
            device_info.getField('sdk_version').setText(deviceInfo['sdk_version'])

    def _set_device_info_callback(self):
        def callback(cls):
            def fun():
                cls.device_chose_widget.setEnabled(False)
                try:
                    device = cls.get_current_device()
                    device_info = cls._get_device_info(device)
                    cls._update_device_info(device_info)
                except AdbBaseError as err:
                    return err
                finally:
                    cls.device_chose_widget.setEnabled(True)
            return fun

        update_thread = Thread()
        update_thread.set_hook(callback(cls=self))
        update_thread.connect(self.raise_dialog)

        self.device_chose_widget.activated.connect(lambda: update_thread.start())
        self.device_chose_widget.currentIndexChanged.connect(lambda: update_thread.start())

    def get_current_device(self) -> ADBDevice:
        current_device_id = self.device_chose_widget.currentText()
        return ADBDevice(current_device_id)

    def raise_dialog(self, exceptions):
        if isinstance(exceptions, AdbBaseError):
            logger.error(str(exceptions))
            dialog = InfoDialog(text='错误', infomativeText=str(exceptions), parent=self)
            dialog.open()
