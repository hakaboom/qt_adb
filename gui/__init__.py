# -*- coding: utf-8 -*-
import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, QPoint, QRect
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import *
from adbutils import ADBDevice, ADBClient
from adbutils.extra.apk import Apk
from adbutils.exceptions import AdbBaseError, AdbInstallError, NoDeviceSpecifyError
from baseImage import IMAGE
from loguru import logger

import src.layout.widget
from css.constant import QSSLoader

from src import (BaseControl, ComboBoxWithButton, CustomLabel, CustomButton, CustomComboBox)
from src.layout.BaseLayout import CustomFormLayout, CustomGridLayout
from src.layout.widget import FormLayoutWidget, GridLayoutWidget, VBoxLayoutWidget, HBoxLayoutWidget
from src.layout.widget import FormLayoutWidget
from css.constant import APK_ICON_HEIGHT, APK_ICON_WIDTH
from gui.thread import Thread, LoopThread
from gui.type_hint import type_device_app_manage_widget
from src.custom_dialog import InfoDialog, QuestionDialog

from typing import Dict, Union, Tuple, List
from functools import wraps


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        self.resize(QSize(960, 540))
        # self.setFixedSize(self.width(), self.height())
        self.setFont(QFont("Microsoft YaHei"))

        style_file = './css/style.qss'
        style_sheet = QSSLoader.read_qss_file(style_file)
        self.setStyleSheet(style_sheet)

        self.enabledManager = EnabledManager()
        # main_widget 布局: 水平布局
        self.main_widget = HBoxLayoutWidget(parent=self, objectName='main_widget')
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("test")

        # 功能栏 布局: 无
        self.function_bar = QWidget(objectName='function_bar')

        # 设备区域 布局: 水平布局
        self.device_main = HBoxLayoutWidget(parent=self.main_widget, objectName='device_main')

        self.main_widget.addWidget(self.function_bar, stretch=1)
        self.main_widget.addWidget(self.device_main, stretch=9)

        # 设备区域控件 布局: 垂直布局
        self.device_config_widget = VBoxLayoutWidget(parent=self.device_main, objectName='device_config')
        self.device_tool_widget = VBoxLayoutWidget(parent=self.device_main, objectName='device_tool')

        self.device_main.addWidget(self.device_config_widget, 3)
        self.device_main.addWidget(self.device_tool_widget, 8)

        # 设备选择控件 布局: 垂直布局----------------------------------------------------------------------------------------
        self.device_chose_control = BaseControl(title='设备选择', objectName='device_chose_control',
                                                widget_flag=lambda: ComboBoxWithButton(btn_text='刷新设备'))
        self.device_chose_control.widget.comboBox.setMinimumHeight(30)
        self.device_chose_control.widget.button.setMinimumHeight(30)
        self.device_chose_control.widget.button.setToolTip('点击后刷新设备列表')
        self.device_chose_widget = self.device_chose_control.widget
        self.enabledManager.addWidget(self.device_chose_widget, index='device_chose')
        self._set_device_chose_callback()

        # 设备信息控件 布局：垂直布局----------------------------------------------------------------------------------------
        self.device_info_control = BaseControl(title='设备信息', objectName='device_info_control',
                                               widget_flag=src.layout.widget.FormLayoutWidgetFlag)
        self.device_info_widget = self._create_device_info_widget(parent=self.device_info_control.widget)
        self._set_device_info_callback()

        self.device_config_widget.addWidget(self.device_chose_control)
        self.device_config_widget.addWidget(self.device_info_control)
        self.device_config_widget.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # 应用管理-------------------------------------------------------------------------------------------------------
        self.device_app_control = BaseControl(title='应用管理', objectName='device_app_control',
                                              widget_flag=src.layout.widget.VBoxLayoutWidgetFlag)
        self.device_app_manage_widget = self._create_device_app_manage_widget(parent=self.device_app_control.widget)
        self._set_app_manage_tools_callback()

        tools_widget = self.device_app_manage_widget.tools
        self.enabledManager.addWidget(tools_widget.getField('foreground_app'), index='foreground_app')
        self.enabledManager.addWidget(tools_widget.getField('stop_app'), index='stop_app')
        self.enabledManager.addWidget(tools_widget.getField('start_app'), index='start_app')
        self.enabledManager.addWidget(tools_widget.getField('clear_app'), index='clear_app')
        self.enabledManager.addWidget(tools_widget.getField('logcat_app'), index='logcat_app')
        self.enabledManager.addWidget(tools_widget.getField('uninstall_app'), index='uninstall_app')
        self.enabledManager.addWidget(tools_widget.getField('save_apk'), index='save_apk')

        self.device_tool_widget.addWidget(self.device_app_control)
        self.device_tool_widget.layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

    @staticmethod
    def _create_device_info_widget(parent: FormLayoutWidget):
        parent.layout.setVerticalSpacing(15)
        loading_tips = '读取中...'
        parent.addRow('设备标识:', CustomLabel(loading_tips), index='serialno')
        parent.addRow('手机型号:', CustomLabel(loading_tips), index='model')
        parent.addRow('手机厂商:', CustomLabel(loading_tips), index='manufacturer')
        parent.addRow('内存容量:', CustomLabel(loading_tips), index='memory')
        parent.addRow('分辨率:', CustomLabel(loading_tips), index='displaySize')
        parent.addRow('安卓版本:', CustomLabel(loading_tips), index='android_version')
        parent.addRow('SDK版本:', CustomLabel(loading_tips), index='sdk_version')

        return parent

    @staticmethod
    def _create_device_app_manage_widget(parent: VBoxLayoutWidget) -> type_device_app_manage_widget:
        parent.setContentsMargins(0, 0, 0, 0)
        parent.layout.setSpacing(0)

        _widget = type_device_app_manage_widget()
        # icon控件
        icon_widget = HBoxLayoutWidget(parent)

        _widget.icon = CustomLabel(parent=icon_widget).\
            setMinimumHeight(APK_ICON_HEIGHT).setMinimumWidth(APK_ICON_WIDTH).\
            setMaximumHeight(APK_ICON_HEIGHT).setMaximumWidth(APK_ICON_WIDTH)
        _widget.icon.setProperty('name', 'apk_icon_widget')

        _widget.tools = GridLayoutWidget(parent=icon_widget)

        _widget.tools.addWidget(CustomButton(text='启动').setMinimumHeight(30), 0, 0, index='start_app')
        _widget.tools.addWidget(CustomButton(text='停止').setMinimumHeight(30), 0, 1, index='stop_app')
        _widget.tools.addWidget(CustomButton(text='清理缓存').setMinimumHeight(30), 0, 2, index='clear_app')
        _widget.tools.addWidget(CustomButton(text='卸载').setMinimumHeight(30), 0, 3, index='uninstall_app')
        _widget.tools.addWidget(CustomButton(text='获取日志').setMinimumHeight(30), 1, 0, index='logcat_app')
        _widget.tools.addWidget(CustomButton(text='切换到当前APP').setMinimumHeight(30), 1, 1, index='foreground_app')
        _widget.tools.addWidget(CustomButton(text='备份Apk').setMinimumHeight(30), 1, 2, index='save_apk')

        icon_widget.addWidget(_widget.icon, 1)
        icon_widget.addWidget(_widget.tools, 4)
        icon_widget.layout.setContentsMargins(6, 6, 6, 6)

        # info控件
        info_widget = VBoxLayoutWidget(parent=parent, objectName='apk_info_widget')

        info_button_widget = HBoxLayoutWidget(parent=info_widget, objectName='apk_info_button')
        info_top_widget = FormLayoutWidget(parent=info_widget, objectName='apk_top_widget')
        info_widget.addWidget(info_top_widget)
        info_widget.addWidget(info_button_widget)
        info_widget.layout.setContentsMargins(0, 0, 0, 0)
        info_widget.layout.setSpacing(0)

        loading_tips = '读取中...'
        # info_top中摆放一些字段较长的类
        _widget.info_top = info_top_widget
        info_top_widget.addRow('应用名称：', CustomLabel(), index='app_label_name')
        info_top_widget.addRow('应用包名：', CustomLabel(), index='app_package_name')
        info_top_widget.addRow('主Activity：', CustomLabel(), index='app_main_activity')
        info_top_widget.layout.setRowWrapPolicy(QFormLayout.WrapLongRows)
        info_top_widget.layout.setContentsMargins(0, 10, 0, 10)
        info_top_widget.layout.setSpacing(10)

        # 左右各一个控件,摆放一些普通字段

        _widget.info_left = FormLayoutWidget(parent=info_button_widget)
        _widget.info_right = FormLayoutWidget(parent=info_button_widget)
        info_button_widget.addWidget(_widget.info_left)
        info_button_widget.addWidget(_widget.info_right)

        _widget.info_left.addRow('版本号：', CustomLabel(), index='app_version_id')
        _widget.info_left.addRow('版本名：', CustomLabel(), index='app_version_name')

        _widget.info_right.addRow('包大小：', CustomLabel(), index='package_size')

        parent.addWidget(icon_widget)
        parent.addWidget(info_widget)

        return _widget

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
            device_info.getField('serialno').setText(deviceInfo['serialno'])
            device_info.getField('model').setText(deviceInfo['model'])
            device_info.getField('manufacturer').setText(deviceInfo['manufacturer'])
            device_info.getField('memory').setText(deviceInfo['memory'])
            device_info.getField('displaySize').setText(deviceInfo['displaySize'])
            device_info.getField('android_version').setText(deviceInfo['android_version'])
            device_info.getField('sdk_version').setText(deviceInfo['sdk_version'])

    def _update_app_info(self, apk: Apk):
        if isinstance(apk, Apk):
            icon: CustomLabel = self.device_app_manage_widget.icon
            info_top: CustomFormLayout = self.device_app_manage_widget.info_top
            info_left: CustomFormLayout = self.device_app_manage_widget.info_left
            info_right: CustomFormLayout = self.device_app_manage_widget.info_right

            icon_local_path = f'./icon/{apk.packageName}.png'
            apk.get_icon_file(local=icon_local_path)
            icon.setPixmap(IMAGE(img=icon_local_path).resize(APK_ICON_WIDTH, APK_ICON_HEIGHT))

            info_top.getField('app_label_name').setText(apk.name)
            info_top.getField('app_package_name').setText(apk.packageName)
            info_top.getField('app_main_activity').setText(apk.main_activity)
            info_left.getField('app_version_id').setText(apk.version_code)
            info_left.getField('app_version_name').setText(apk.version_name)
            package_size = f'{(apk.device.get_file_size(remote=apk.install_path) / 1024):.1f}MB'
            info_right.getField('package_size').setText(package_size)

    def reconfirm(self, hook, text: str = '确认是否进行操作'):
        def fun():
            dialog = QuestionDialog(text=text, parent=self)
            dialog.add_yesRole_hook(hook)
            dialog.open()
        return fun

    # --------------callback
    def _set_device_chose_callback(self):
        """ 使用device_chose控件进行回调 """
        # 使用控件self.device_chose_control,绑定btn回调,向comboBox中刷新组件
        client = ADBClient()

        def callback(adb: ADBClient, cls):
            def fun():
                logger.debug('刷新设备')
                cls.enabledManager.all_unavailable()
                current_device = cls.device_chose_control.widget.comboBox.currentText()
                # step1: 清除所有item
                cls.device_chose_control.widget.comboBox.clear()

                # step2: 讲选中设备,重新添加进item
                if current_device:
                    cls.device_chose_control.widget.comboBox.addItem(current_device)

                # 从adb devices中,获取最新的设备信息
                devices = adb.devices
                logger.debug(devices)
                for device_id, state in devices.items():
                    if state != 'device' or device_id == current_device:
                        continue
                    cls.device_chose_control.widget.comboBox.addItem(device_id)

                cls.enabledManager.all_available()

            return fun

        update_thread = Thread(exceptions=(AdbBaseError,))
        update_thread.add_hook(callback(adb=client, cls=self))
        update_thread.add_exception_hook(AdbBaseError, self.raise_dialog)
        self.device_chose_control.widget.button.set_click_hook(update_thread.start)

    def _set_foreground_app_callback(self):
        btn: CustomButton = self.device_app_manage_widget.tools.getField('foreground_app')
        def callback(cls):
            @self.freeze(index=['start_app', 'stop_app', 'clear_app', 'uninstall_app', 'foreground_app', 'logcat_app', 'save_apk'])
            def fun():
                device: ADBDevice = cls.get_current_device()
                apk = Apk(device=device, packageName=device.foreground_package)
                cls._update_app_info(apk)
            return fun

        update_thread = Thread(exceptions=(AdbBaseError,))
        update_thread.add_hook(callback(cls=self))
        update_thread.add_exception_hook(AdbBaseError, self.raise_dialog)

        btn.set_click_hook(update_thread.start)

    def _set_uninstall_app_callback(self):
        btn: CustomButton = self.device_app_manage_widget.tools.getField('uninstall_app')

        def callback(cls):
            @self.freeze(index=['start_app', 'stop_app', 'clear_app', 'uninstall_app', 'foreground_app', 'logcat_app', 'save_apk'])
            def fun():
                device: ADBDevice = cls.get_current_device()
                if packageName := cls.get_current_app_manage_packageName():
                    device.uninstall(package_name=packageName)
            return fun

        update_thread = Thread(exceptions=(AdbBaseError,))
        update_thread.add_hook(callback(cls=self))
        update_thread.add_exception_hook(AdbBaseError, self.raise_dialog)

        btn.set_click_hook(self.reconfirm(update_thread.start))

    def _set_stop_app_callback(self):
        btn: CustomButton = self.device_app_manage_widget.tools.getField('stop_app')

        def callback(cls):
            @self.freeze(index=['start_app', 'stop_app', 'clear_app', 'uninstall_app', 'foreground_app', 'logcat_app', 'save_apk'])
            def fun():
                device: ADBDevice = cls.get_current_device()
                if packageName := cls.get_current_app_manage_packageName():
                    device.stop_app(package=packageName)
            return fun

        update_thread = Thread(exceptions=(AdbBaseError,))
        update_thread.add_hook(callback(cls=self))
        update_thread.add_exception_hook(AdbBaseError, self.raise_dialog)

        btn.set_click_hook(self.reconfirm(update_thread.start))

    def _set_start_app_callback(self):
        btn: CustomButton = self.device_app_manage_widget.tools.getField('start_app')

        def callback(cls):
            @self.freeze(index=['start_app', 'stop_app', 'clear_app', 'uninstall_app', 'foreground_app', 'logcat_app', 'save_apk'])
            def fun():
                device: ADBDevice = cls.get_current_device()
                if packageName := cls.get_current_app_manage_packageName():
                    device.start_app(package=packageName)
            return fun

        update_thread = Thread(exceptions=(AdbBaseError,))
        update_thread.add_hook(callback(cls=self))
        update_thread.add_exception_hook(AdbBaseError, self.raise_dialog)

        btn.set_click_hook(update_thread.start)

    def _set_clear_app_callback(self):
        btn: CustomButton = self.device_app_manage_widget.tools.getField('clear_app')

        def callback(cls):
            @self.freeze(index=['start_app', 'stop_app', 'clear_app', 'uninstall_app', 'foreground_app', 'logcat_app',
                                'save_apk'])
            def fun():
                device: ADBDevice = cls.get_current_device()
                if packageName := cls.get_current_app_manage_packageName():
                    device.clear_app(package=packageName)
            return fun

        update_thread = Thread(exceptions=(AdbBaseError,))
        update_thread.add_hook(callback(cls=self))
        update_thread.add_exception_hook(AdbBaseError, self.raise_dialog)

        btn.set_click_hook(self.reconfirm(update_thread.start))

    def _set_save_apk_callback(self):
        btn: CustomButton = self.device_app_manage_widget.tools.getField('save_apk')

        def callback(cls):
            @self.freeze(index=['start_app', 'stop_app', 'clear_app', 'uninstall_app', 'foreground_app', 'logcat_app', 'save_apk'])
            def fun():
                device: ADBDevice = cls.get_current_device()
                if packageName := cls.get_current_app_manage_packageName():
                    path = device.get_app_install_path(packageName=packageName)
                    print(path)
            return fun

        update_thread = Thread(exceptions=(AdbBaseError,))
        update_thread.add_hook(callback(cls=self))
        update_thread.add_exception_hook(AdbBaseError, self.raise_dialog)

        btn.set_click_hook(self.reconfirm(update_thread.start))

    def _set_app_manage_tools_callback(self):
        self._set_foreground_app_callback()
        self._set_stop_app_callback()
        self._set_start_app_callback()
        self._set_clear_app_callback()
        self._set_uninstall_app_callback()
        self._set_save_apk_callback()

    def _set_device_info_callback(self):
        def callback(cls):
            def fun():
                cls.device_chose_widget.setEnabled(False)
                device = cls.get_current_device()
                device_info = cls._get_device_info(device)
                cls._update_device_info(device_info)
                cls.device_chose_widget.setEnabled(True)
            return fun

        update_thread = Thread(exceptions=(AdbBaseError,))
        update_thread.add_hook(callback(cls=self))
        update_thread.add_exception_hook(AdbBaseError, self.raise_dialog)

        self.device_chose_widget.comboBox.activated.connect(lambda: update_thread.start())
        self.device_chose_widget.comboBox.currentIndexChanged.connect(lambda: update_thread.start())

    # --------------
    def get_current_device(self) -> ADBDevice:
        current_device_id = self.device_chose_widget.comboBox.currentText()
        return ADBDevice(current_device_id)

    def get_current_app_manage_packageName(self) -> str:
        return self.device_app_manage_widget.info_top.getField('app_package_name').text()

    def get_current_app_manage_mainActivity(self) -> str:
        return self.device_app_manage_widget.info_top.getField('app_main_activity').text()

    def raise_dialog(self, exceptions):
        logger.error(str(exceptions))
        dialog = InfoDialog(text='错误', infomativeText=str(exceptions), parent=self)
        dialog.open()

    def freeze(self, index: Union[str, Tuple[str, ...], List[str]] = None):
        def freeze_decorator(func):
            @wraps(func)
            def wrapped_function(*args, **kwargs):
                try:
                    if index == 'ALL':
                        self.enabledManager.all_unavailable()
                    elif isinstance(index, (Tuple, List)):
                        self.enabledManager.set_widget_unavailable(index=index)
                    return func(*args, **kwargs)
                finally:
                    if index == 'ALL':
                        self.enabledManager.all_available()
                    elif isinstance(index, (Tuple, List)):
                        self.enabledManager.set_widget_available(index=index)
            return wrapped_function
        return freeze_decorator


class EnabledManager(object):
    """
    用于管理控件enable状态
    """

    def __init__(self):
        self.widgets: Dict[str, QWidget] = {}

    def addWidget(self, widget: QWidget, index=None):
        self.widgets[index or str(widget)] = widget

    def all_available(self):
        """
        设置所有控件 Enable属性为True

        Returns:
            None
        """
        for widget in self.widgets.values():
            widget.setEnabled(True)

    def all_unavailable(self):
        """
        设置所有控件 Enable属性为False

        Returns:
            None
        """
        for widget in self.widgets.values():
            widget.setEnabled(False)

    def get_widget(self, index):
        return self.widgets.get(index)

    def set_widget_available(self, index: Union[str, List[str], Tuple[str, ...]]):
        """
        设置控件 Enable属性为True

        Args:
            index: 需要设置的控件

        Returns:
            None
        """
        items = []
        if isinstance(index, str):
            items += [index]
        elif isinstance(index, (list, tuple)):
            items += index

        for widget_index in items:
            if widget := self.widgets.get(widget_index):
                widget.setEnabled(True)
            else:
                logger.warning(f'未找到控件:{widget_index}')

    def set_widget_unavailable(self, index: Union[str, List[str], Tuple[str, ...]]):
        """
        设置控件 Enable属性为False

        Args:
            index: 需要设置的控件

        Returns:
            None
        """
        items = []
        if isinstance(index, str):
            items += [index]
        elif isinstance(index, (list, tuple)):
            items += index

        for widget_index in items:
            if widget := self.widgets.get(widget_index):
                widget.setEnabled(False)
            else:
                logger.warning(f'未找到控件:{widget_index}')