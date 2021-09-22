# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QLayout
from PyQt5 import QtCore

from src.layout.BaseLayout import CustomGridLayout, CustomVBoxLayout, CustomFormLayout, CustomHBoxLayout

from typing import Union, Type, List, Tuple
from loguru import logger


class BaseObject(QWidget):
    def __init__(self, parent=None, objectName: str = None):
        super(BaseObject, self).__init__(parent)
        self.setObjectName(objectName)

    @property
    def layout(self) -> QLayout:
        return super(BaseObject, self).layout()

    def setFormAlignment(self, flag):
        self.layout.setFormAlignment(flag)
        return self

    def getField(self, index: str):
        return self.layout.getField(index)


class FormLayoutWidget(BaseObject):
    def __init__(self, parent=None, objectName: str = None):
        super(FormLayoutWidget, self).__init__(parent, objectName)
        self.setLayout(CustomFormLayout(parent=self))

    @property
    def layout(self) -> CustomFormLayout:
        return super(BaseObject, self).layout()

    def addRow(self, label: str, field: QWidget = None, index: str = None):
        self.layout.addRow(label=label, field=field, index=index)


class GridLayoutWidget(BaseObject):
    def __init__(self, parent=None, objectName: str = None):
        super(GridLayoutWidget, self).__init__(parent, objectName)
        self.setLayout(CustomGridLayout(parent=self))

    @property
    def layout(self) -> CustomGridLayout:
        return super(BaseObject, self).layout()

    def addWidget(self, w: Type[QWidget], row: int, column: int, rowSpan: int = 1, columnSpan: int = 1,
                  alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = QtCore.Qt.Alignment(),
                  index: str = None) -> None:
        self.layout.addWidget(w, row, column, rowSpan, columnSpan, alignment, index=index)


class VBoxLayoutWidget(BaseObject):
    def __init__(self, parent=None, objectName: str = None):
        super(VBoxLayoutWidget, self).__init__(parent, objectName)
        self.setLayout(CustomVBoxLayout(parent=self))

    @property
    def layout(self) -> CustomVBoxLayout:
        return super(BaseObject, self).layout()

    def addWidget(self, a0: QWidget, stretch: int = ...,
                  alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = ..., index: str = None) -> None:
        self.layout.addWidget(a0, stretch, alignment, index)


class HBoxLayoutWidget(BaseObject):
    def __init__(self, parent=None, objectName: str = None):
        super(HBoxLayoutWidget, self).__init__(parent, objectName)
        self.setLayout(CustomHBoxLayout(parent=self))

    @property
    def layout(self) -> CustomHBoxLayout:
        return super(BaseObject, self).layout()

    def addWidget(self, a0: QWidget, stretch: int = 0,
                  alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = QtCore.Qt.Alignment(),
                  index: str = None) -> None:
        self.layout.addWidget(a0, stretch, alignment, index)
