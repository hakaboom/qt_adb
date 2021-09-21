# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QLayout
from PyQt5 import QtCore

from src.layout.BaseLayout import CustomGridLayout, CustomVBoxLayout, CustomFormLayout, CustomHBoxLayout

from typing import Union, Type, List, Tuple
from loguru import logger


class BaseObject(QWidget):
    def __init__(self, parent=None):
        super(BaseObject, self).__init__(parent)

    @property
    def layout(self) -> QLayout:
        return super(BaseObject, self).layout()

    def setFormAlignment(self, flag):
        self.layout.setFormAlignment(flag)
        return self

    def getField(self, index: str):
        return self.layout.getField(index)


class FormLayoutWidget(BaseObject):
    def __init__(self, parent=None):
        super(FormLayoutWidget, self).__init__(parent)
        self.setLayout(CustomFormLayout(parent=self))

    def addRow(self, label: str, field: QWidget = None, index: str = None):
        self.layout.addRow(label, field, index)


class GridLayoutWidget(QWidget):
    def __init__(self, parent=None):
        super(GridLayoutWidget, self).__init__(parent)
        self.setLayout(CustomGridLayout(parent=self))