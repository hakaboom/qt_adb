# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, QPoint, QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from adbutils import ADBDevice
from adbutils.exceptions import AdbBaseError, AdbInstallError
from loguru import logger


from src.device_group import deviceInfoWidget, deviceToolWidget, deviceChoseWidget
from src.button import CustomButton
from src.fold_widget import foldWidget
from gui.thread import Thread, LoopThread
from src.custom_dialog import InfoDialog


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
        self.function_bar.setStyleSheet('background-color: rgb(0, 170, 255);')
        self.main_layout.addWidget(self.function_bar)

        # 设备区域 布局: 水平布局
        self.device_main = QWidget(objectName='device_main')
        self.main_layout.addWidget(self.device_main)
        self.device_main.setStyleSheet('background-color: rgb(170, 255, 0);')
        self.device_main_layout = QHBoxLayout(self.device_main)
        self.device_main_layout.setObjectName('device_main_layout')

        self.main_layout.setStretch(0, 2)
        self.main_layout.setStretch(1, 9)

        # 设备区域控件 布局: 垂直布局
        self.device_config_widget = QWidget(objectName='device_config')
        self.device_config_widget.setStyleSheet('background-color: rgb(255, 170, 0);')
        self.device_main_layout.addWidget(self.device_config_widget)
        self.device_main_layout.setContentsMargins(5, 5, 5, 5)

        self.device_tool_widget = QWidget(objectName='device_tool')
        self.device_tool_widget.setStyleSheet('background-color: rgb(0, 255, 255);')
        self.device_main_layout.addWidget(self.device_tool_widget)

        self.device_main_layout.setStretch(0, 3)
        self.device_main_layout.setStretch(1, 8)

        self.device_config_layout = QVBoxLayout(self.device_config_widget)
        self.device_config_layout.setContentsMargins(5, 5, 5, 5)

        # 设备选择控件 布局: 垂直布局
        self.device_chose_widget = QWidget(objectName='device_chose')
        self.device_chose_widget.setStyleSheet('background-color: rgb(0, 255, 127);')
        self.device_chose_layout = QVBoxLayout(self.device_chose_widget)
        self.device_chose_layout.setContentsMargins(0, 0, 0, 0)
        self.device_chose_widget.setMaximumHeight(100)
        self.device_chose_widget.setMinimumHeight(100)

        test = BaseControl(title='设备选择')
        self.device_chose_layout.addWidget(test)
        # self.device_chose_label = QLabel('设备选择')
        # self.device_chose_label.setAlignment(QtCore.Qt.AlignCenter)
        # self.device_chose_layout.addWidget(self.device_chose_label)

        self.device_info_widget = QWidget(objectName='device_info')
        self.device_info_widget.setStyleSheet('background-color: rgb(255, 255, 127);')

        self.device_config_layout.addWidget(self.device_chose_widget)
        self.device_config_layout.addWidget(self.device_info_widget)


class BaseControl(QWidget):
    def __init__(self, title: str, parent=None):
        super(BaseControl, self).__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel(title)
        self.title.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.widget = QWidget(self)
        self.widget.setStyleSheet('background-color: rgb(255, 255, 255);')

        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.widget)
