# -*- coding: utf-8 -*-
import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, QPoint, QRect, Qt
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtWidgets import *
from baseImage import IMAGE
from loguru import logger

import src.layout.widget
from src.layout.BaseLayout import CustomGridLayout, CustomFormLayout, CustomHBoxLayout, CustomVBoxLayout
from src.layout.widget import GridLayoutWidget, FormLayoutWidget, HBoxLayoutWidget, VBoxLayoutWidget
from typing import Union, Tuple, List, Type, Callable
from functools import wraps


class BaseControl(VBoxLayoutWidget):
    def __init__(self, title: str, parent=None, objectName=None,
                 widget_flag: Union[int, Type[QWidget], Callable, None] = None):
        super(BaseControl, self).__init__(parent, objectName)
        self._title = CustomLabel(title=title, parent=self)

        if widget_flag == src.layout.widget.FormLayoutWidgetFlag:
            self._widget = FormLayoutWidget(parent=self)
        elif widget_flag == src.layout.widget.HBoxLayoutWidgetFlag:
            self._widget = HBoxLayoutWidget(parent=self)
        elif widget_flag == src.layout.widget.VBoxLayoutWidgetFlag:
            self._widget = VBoxLayoutWidget(parent=self)
        elif widget_flag == src.layout.widget.GridLayoutWidgetFlag:
            self._widget = GridLayoutWidget(parent=self)
        elif isinstance(widget_flag, type(QWidget)):
            self._widget = widget_flag(parent=self)
        elif callable(widget_flag):
            self._widget = widget_flag()
        else:
            self._widget = QWidget(self)

        self._title.setProperty('name', 'baseControl_title')
        self._widget.setProperty('name', 'baseControl_widget')

        self.addWidget(self._title)
        self.addWidget(self._widget)

        self.title.setAlignment(QtCore.Qt.AlignCenter)

    @property
    def title(self):
        return self._title

    @property
    def widget(self):
        return self._widget


class CustomComboBox(QComboBox):
    def __init__(self, item: Union[str, List[str], Tuple[str, ...]] = None, parent=None):
        super(CustomComboBox, self).__init__(parent=parent)
        self.addItem(item)

    def addItem(self, item: Union[str, List[str], Tuple[str, ...]]) -> None:
        if isinstance(item, str):
            super(CustomComboBox, self).addItem(item)
        elif isinstance(item, list):
            super(CustomComboBox, self).addItems(item)

    def getItemsText(self) -> List[str]:
        ret = []
        for index in range(self.count()):
            ret.append(self.itemText(index))

        return ret

    @property
    def layout(self):
        return self._layout


class ComboBoxWithButton(HBoxLayoutWidget):
    def __init__(self, item: Union[str, List[str], Tuple[str, ...]] = None, btn_text: str = None,
                 parent: QWidget = None):
        super(ComboBoxWithButton, self).__init__(parent=parent)
        self._button = CustomButton(text=btn_text, parent=self)
        self._comboBox = CustomComboBox(item=item, parent=self)

        self.addWidget(self.comboBox, 6)
        self.addWidget(self.button, 1)

    @property
    def comboBox(self):
        return self._comboBox

    @property
    def button(self):
        return self._button

    def addItem(self, item: Union[str, List[str], Tuple[str, ...]]) -> None:
        self.comboBox.addItem(item)


class CustomLabel(QLabel):
    def __init__(self, title: Union[QPixmap, IMAGE, QImage, str] = None, parent=None, styleSheet=None):
        super(CustomLabel, self).__init__(parent)
        if isinstance(title, str):
            self.setText(title)
        elif isinstance(title, (QPixmap, IMAGE, QImage)):
            self.setPixmap(title)

        self.setStyleSheet(styleSheet)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def setMinimumSize(self, *__args):
        super(CustomLabel, self).setMinimumSize(__args)
        return self

    def setMinimumHeight(self, p_int):
        super(CustomLabel, self).setMinimumHeight(p_int)
        return self

    def setMinimumWidth(self, p_int):
        super(CustomLabel, self).setMinimumWidth(p_int)
        return self

    def setMaximumHeight(self, p_int):
        super(CustomLabel, self).setMaximumHeight(p_int)
        return self

    def setMaximumWidth(self, p_int):
        super(CustomLabel, self).setMaximumWidth(p_int)
        return self

    def setPixmap(self, a0: Union[QPixmap, IMAGE, QImage]) -> None:
        if isinstance(a0, IMAGE):
            pixmap = QPixmap(cv_to_qtimg(a0))
        elif isinstance(a0, QImage):
            pixmap = QPixmap(QImage)
        elif isinstance(a0, QPixmap):
            pixmap = a0
        else:
            raise ValueError(f'a0 type=<{type(a0)}>, need QPixmap, IMAGE, QImage')

        super(CustomLabel, self).setPixmap(pixmap)

    def setText(self, a0: str) -> None:
        super(CustomLabel, self).setText(str(a0))


class CustomButton(QPushButton):
    # 按钮作为开关
    def __init__(self, text: str = None, item=None, hook=None, icon=None, parent=None):
        param = [icon, text, parent]
        super(CustomButton, self).__init__(*list(filter(None, param)))
        self.item = item
        self.hook = hook
        self.clicked.connect(self.run)

    def setStyleSheet(self, p_str):
        super(CustomButton, self).setStyleSheet(p_str)
        return self

    def setMinimumSize(self, *__args):
        super(CustomButton, self).setMinimumSize(__args)
        return self

    def setMinimumHeight(self, p_int):
        super(CustomButton, self).setMinimumHeight(p_int)
        return self

    def setMinimumWidth(self, p_int):
        super(CustomButton, self).setMinimumWidth(p_int)
        return self

    def resizeEvent(self, event):
        # 解决item的高度问题
        super(CustomButton, self).resizeEvent(event)
        if self.item:
            self.item.setSizeHint(QSize(self.minimumWidth(), self.height()))

    def set_click_hook(self, hook):
        self.hook = hook

    def run(self):
        if callable(self.hook):
            return self.hook()


def cv_to_qtimg(img: IMAGE):
    height, width, depth = img.shape
    img = img.cvtColor(cv2.COLOR_BGR2RGB)
    return QImage(img.data, width, height, width * depth, QImage.Format_RGB888)
