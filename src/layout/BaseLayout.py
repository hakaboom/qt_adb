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

    def _addRow(self, index, field: QWidget):
        if index:
            self.rows[index] = field
        elif field.objectName():
            self.rows[field.objectName()] = field
        # else:
        #     logger.warning(f'object:\'{self.parent().objectName()}\' 未设置索引')


class CustomFormLayout(QFormLayout, BaseLayout):
    def __init__(self, parent=None):
        super(CustomFormLayout, self).__init__(parent)
        self.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setLabelAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

    def addRow(self, label: Union[str, QWidget] = None, field: QWidget = None, index: str = None) -> None:
        super(CustomFormLayout, self).addRow(label, field)
        self._addRow(index=index, field=field)


class CustomGridLayout(QGridLayout, BaseLayout):
    def __init__(self, parent=None):
        super(CustomGridLayout, self).__init__(parent=parent)

    def addWidget(self, w: Type[QWidget], row: int, column: int, rowSpan: int = 1, columnSpan: int = 1,
                  alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = QtCore.Qt.Alignment(),
                  index: str = None) -> None:
        super(CustomGridLayout, self).addWidget(w, row, column, rowSpan, columnSpan, alignment)
        self._addRow(index=index, field=w)


class CustomVBoxLayout(QVBoxLayout, BaseLayout):
    def __init__(self, parent=None):
        super(CustomVBoxLayout, self).__init__(parent=parent)

    def addWidget(self, a0: QWidget, stretch: int = 0,
                  alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = QtCore.Qt.Alignment(),
                  index: str = None) -> None:
        super(CustomVBoxLayout, self).addWidget(a0, stretch, alignment)
        self._addRow(index=index, field=a0)


class CustomHBoxLayout(QHBoxLayout, BaseLayout):
    def __init__(self, parent=None):
        super(CustomHBoxLayout, self).__init__(parent=parent)

    def addWidget(self, a0: QWidget, stretch: int = 0,
                  alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = QtCore.Qt.Alignment(),
                  index: str = None) -> None:
        super(CustomHBoxLayout, self).addWidget(a0, stretch, alignment)
        self._addRow(index=index, field=a0)
