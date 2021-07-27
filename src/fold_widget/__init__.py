# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from loguru import logger
from src.button import CustomButton
from typing import List


class foldWidget(QListWidget):
    def __init__(self, parent=None):
        super(foldWidget, self).__init__(parent)
        self.setMinimumWidth(150)
        self.setMaximumWidth(150)

        self.button_list = []

    def get_button_list(self) -> List[CustomButton]:
        return self.button_list

    def add_button(self, item, button):
        self.setItemWidget(item, button)
        self.button_list.append(button)
