# -*- coding: utf-8 -*-
import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, QPoint, QRect, Qt
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtWidgets import *
from baseImage import IMAGE
from loguru import logger

from typing import Union, Tuple, List, Type
from functools import wraps


class BaseControl(QWidget):
    def __init__(self, title: str, objectName: str = None, parent=None):
        """
        基础模块控件
        垂直布局,包含一个标题和一个QWidget

        Args:
            title: 标题文字
            parent: 父控件
        """
        super(BaseControl, self).__init__(parent, objectName=objectName)

        self.main_layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self._title = CustomLabel(title)
        self._widget = QWidget(self)
        self._widget.setContentsMargins(0, 0, 0, 0)

        self._title.setProperty('name', 'baseControl_title')
        self._widget.setProperty('name', 'baseControl_widget')

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.widget)

        self.title.setAlignment(QtCore.Qt.AlignCenter)

    @property
    def layout(self):
        return self.main_layout

    @property
    def title(self):
        return self._title

    @property
    def widget(self):
        return self._widget

    def setStretch(self, index: int, stretch: int):
        self.layout.setStretch(index, stretch)

    def addSpacerItem(self, spacerItem: QSpacerItem):
        self.layout.addSpacerItem(spacerItem)


class CustomComboBox(QWidget):
    def __init__(self, item: Union[str, List[str], Tuple[str, ...]] = None, parent=None):
        super(CustomComboBox, self).__init__(parent=parent)

        self.comboBox = QComboBox(parent=self)
        self._layout = QHBoxLayout(parent)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.addItem(item)

    def getItemsText(self) -> List[str]:
        ret = []
        for index in range(self.comboBox.count()):
            ret.append(self.comboBox.itemText(index))

        return ret

    def currentText(self):
        return self.comboBox.currentText()

    def currentIndex(self):
        return self.comboBox.currentIndex()

    def clear(self):
        self.comboBox.clear()

    @property
    def currentIndexChanged(self):
        return self.comboBox.currentIndexChanged

    @property
    def activated(self):
        return self.comboBox.activated

    @property
    def layout(self):
        return self._layout

    def setStretch(self, index: int, stretch: int):
        self.layout.setStretch(index, stretch)

    def addItem(self, item: Union[str, list]):
        """ 向comboBox中添加item"""
        if isinstance(item, str):
            self.comboBox.addItem(item)
        elif isinstance(item, list):
            self.comboBox.addItems(item)


class ComboBoxWithButton(CustomComboBox):
    """
        Activated	当用户选中一个下拉选项时发射该信号
        currentIndexChanged	当下拉选项的索引发生改变时发射该信号
        highlighted	当选中一个已经选中的下拉选项时，发射该信号

    """
    def __init__(self, item: Union[str, List[str], Tuple[str, ...]] = None, btn_text: str = None,
                 parent: QWidget = None):
        super(ComboBoxWithButton, self).__init__(item=item, parent=parent)

        self.btn = CustomButton(text=btn_text, parent=self)

        self.comboBox.setProperty('name', 'ComboBoxWithButton_comboBox')
        self.btn.setProperty('name', 'ComboBoxWithButton_btn')

        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.btn)

        self.setStretch(0, 6)
        self.setStretch(0, 1)

    def setEnabled(self, flag: bool):
        """ 设置按钮和下拉框是否可以点击 """
        self.btn.setEnabled(flag)
        self.comboBox.setEnabled(flag)


class CustomFormLayout(QFormLayout):
    def __init__(self, parent=None):
        super(CustomFormLayout, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setLabelAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.rows = {}

    def setFormAlignment(self, flag):
        super(CustomFormLayout, self).setFormAlignment(flag)
        return self

    def addRow(self, label: str, field: QWidget = None, index: str = None):
        super(CustomFormLayout, self).addRow(label, field)
        self.rows[index or label] = field

    def getField(self, index: str):
        return self.rows.get(index)

    def update_label(self, title, value):
        if self.rows.get(title):
            self.rows[title].setText(str(value))


class CustomGridLayout(QGridLayout):
    def __init__(self, parent=None):
        super(CustomGridLayout, self).__init__(parent)
        self.rows = {}

    def addWidget(self, w: Type[QWidget], row: int, column: int, rowSpan: int = 1, columnSpan: int = 1,
                  alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = Qt.Alignment(),
                  index: str = None):
        super(CustomGridLayout, self).addWidget(w, row, column, rowSpan, columnSpan, alignment)
        self.rows[index or str(w)] = w

    def getField(self, index: Union[str, QWidget]):
        if field := self.rows.get(str(index)):
            return field
        else:
            logger.warning(f'未能在找到index:{str(index)}')


class FormLayoutWidget(QWidget):
    def __init__(self, parent=None):
        super(FormLayoutWidget, self).__init__(parent)
        self.setLayout(CustomFormLayout(parent=self))
        self.rows = {}

    @property
    def layout(self) -> CustomFormLayout:
        return super(FormLayoutWidget, self).layout()

    def setFormAlignment(self, flag):
        self.layout.setFormAlignment(flag)
        return self

    def addRow(self, label: str, field: QWidget = None, index: str = None):
        self.layout.addRow(label, field)
        self.rows[index or label] = field

    def getField(self, index: str):
        return self.rows.get(index)

    def update_label(self, title, value):
        if self.rows.get(title):
            self.rows[title].setText(str(value))


class CustomLabel(QLabel):
    def __init__(self, title: Union[QPixmap, IMAGE, QImage, str] = None, parent=None, styleSheet=None):
        super(CustomLabel, self).__init__(parent=parent)
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
