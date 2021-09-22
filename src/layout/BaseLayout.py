# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFormLayout, QGridLayout, QHBoxLayout, QVBoxLayout, QLayout, QWidget
from PyQt5 import QtCore

from typing import Union, Type, List, Tuple
from loguru import logger


class BaseLayout(QLayout):
    def __init__(self, parent=None):
        super(BaseLayout, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.rows = {}  # 存放控件

    def getField(self, index: str):
        return self.rows.get(index)


class CustomFormLayout(QFormLayout, BaseLayout):
    def __init__(self, parent=None):
        super(CustomFormLayout, self).__init__(parent)
        self.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setLabelAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

    def addRow(self, label: Union[str, QWidget] = None, field: QWidget = None, index: str = None) -> None:
        super(CustomFormLayout, self).addRow(label, field)
        if index:
            self.rows[index] = field
        else:
            logger.warning(f'label:\'{label}\' 未设置索引')


class CustomGridLayout(QGridLayout, BaseLayout):
    def __init__(self, parent=None):
        super(CustomGridLayout, self).__init__(parent=parent)

    def addWidget(self, w: Type[QWidget], row: int, column: int, rowSpan: int = 1, columnSpan: int = 1,
                  alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = QtCore.Qt.Alignment(),
                  index: str = None) -> None:
        super(CustomGridLayout, self).addWidget(w, row, column, rowSpan, columnSpan, alignment)
        if index:
            self.rows[index] = w
        else:
            logger.warning(f'label:\'{w}\' row:{row}, column:{column} 未设置索引')


class CustomVBoxLayout(QVBoxLayout, BaseLayout):
    def __init__(self, parent=None):
        super(CustomVBoxLayout, self).__init__(parent=parent)

    def addWidget(self, a0: QWidget, stretch: int = ...,
                  alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = ..., index: str = None) -> None:
        super(CustomVBoxLayout, self).addWidget(a0, stretch, alignment)
        if index:
            self.rows[index] = a0
        else:
            logger.warning(f'widget:\'{a0}\' 未设置索引')


class CustomHBoxLayout(QHBoxLayout, BaseLayout):
    def __init__(self, parent=None):
        super(CustomHBoxLayout, self).__init__(parent=parent)

    def addWidget(self, a0: QWidget, stretch: int = 0,
                  alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = QtCore.Qt.Alignment(),
                  index: str = None) -> None:
        super(CustomHBoxLayout, self).addWidget(a0, stretch, alignment)
        if index:
            self.rows[index] = a0
        else:
            logger.warning(f'widget:\'{a0}\' 未设置索引')
