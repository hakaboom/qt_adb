# -*- coding: utf-8 -*-
import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, QPoint, QRect, Qt
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtWidgets import *
from baseImage import IMAGE
from loguru import logger

from src.button import CustomButton
from src.fold_widget import foldWidget
from src.custom_dialog import InfoDialog

from typing import Union, Tuple, List


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
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.title = Label(title)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.widget = QWidget(self)

        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.widget)
        # self.widget.setStyleSheet('background-color: rgb(255, 255, 127);')
        self.title.setMaximumHeight(30)

    def setStretch(self, index: int, stretch: int):
        self.main_layout.setStretch(index, stretch)

    def addSpacerItem(self, spacerItem: QSpacerItem):
        self.main_layout.addSpacerItem(spacerItem)


class ComboBoxWithButton(object):
    """
        Activated	当用户选中一个下拉选项时发射该信号
        currentIndexChanged	当下拉选项的索引发生改变时发射该信号
        highlighted	当选中一个已经选中的下拉选项时，发射该信号

    """

    def __init__(self, item: Union[str, List[str], Tuple[str, ...]] = None, btn_text: str = None,
                 parent: QWidget = None):
        self.comboBox = QComboBox()
        self.btn = CustomButton(text=btn_text, parent=parent)
        self.addItem(item)

        self.main_layout = QHBoxLayout(parent)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addWidget(self.comboBox)
        self.main_layout.addWidget(self.btn)

        self.setStretch(0, 6)
        self.setStretch(0, 1)

    def setStretch(self, index: int, stretch: int):
        self.main_layout.setStretch(index, stretch)

    def addItem(self, item: Union[str, list]):
        """ 向comboBox中添加item"""
        if isinstance(item, str):
            self.comboBox.addItem(item)
        elif isinstance(item, list):
            self.comboBox.addItems(item)

    def setEnabled(self, flag: bool):
        """ 设置按钮和下拉框是否可以点击 """
        self.btn.setEnabled(flag)
        self.comboBox.setEnabled(flag)

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


class FormLayout(QWidget):
    def __init__(self, parent=None):
        super(FormLayout, self).__init__(parent=parent)

        self.main_layout = QFormLayout(parent)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # self.main_layout.setFormAlignment(Qt.AlignTop)
        # self.main_layout.setLabelAlignment(Qt.AlignCenter)
        self.rows = {}

    def addRow(self, label: str, field: QWidget = None, index: str = None):
        self.main_layout.addRow(label, field)
        self.rows[index or label] = field

    def getField(self, index: str):
        return self.rows.get(index)

    def update_label(self, title, value):
        if self.rows.get(title):
            self.rows[title].setText(str(value))


class GridLayout(QWidget):
    def __init__(self, parent=None):
        super(GridLayout, self).__init__(parent=parent)
        self.setStyleSheet('background-color: rgb(0, 255, 255);')

        # self.main_layout = QFormLayout(parent)
        # self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.rows = {}

    def addWidget(self, w: QWidget, row: int, column: int, rowSpan: int = 1, columnSpan: int = 1,
                  alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = Qt.Alignment(), index: str = None):
        self.main_layout.addWidget(w, row, column, rowSpan, columnSpan, alignment)
        self.rows[index or str(w)] = w

    def getField(self, index: Union[str, QWidget]):
        return self.rows.get(str(index))


class Label(QLabel):
    def __init__(self, title: Union[QPixmap, IMAGE, QImage, str] = None, parent=None):
        super(Label, self).__init__(parent=parent)
        if isinstance(title, str):
            self.setText(title)
        elif isinstance(title, (QPixmap, IMAGE, QImage)):
            self.setPixmap(title)

        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def setPixmap(self, a0: Union[QPixmap, IMAGE, QImage]) -> None:
        if isinstance(a0, IMAGE):
            pixmap = QPixmap(cv_to_qtimg(a0))
        elif isinstance(a0, QImage):
            pixmap = QPixmap(QImage)
        elif isinstance(a0, QPixmap):
            pixmap = a0
        else:
            raise ValueError(f'a0 type=<{type(a0)}>, need QPixmap, IMAGE, QImage')

        super(Label, self).setPixmap(pixmap)

    def setText(self, a0: str) -> None:
        super(Label, self).setText(str(a0))


def cv_to_qtimg(img: IMAGE):
    height, width, depth = img.shape
    img = img.cvtColor(cv2.COLOR_BGR2RGB)
    return QImage(img.data, width, height, width * depth, QImage.Format_RGB888)
