# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from loguru import logger


class foldWidget(QListWidget):
    def __init__(self, parent=None):
        super(foldWidget, self).__init__(parent)
        self.setMinimumWidth(120)
        self.setMaximumWidth(120)

        self.button_item = []
        # 读取工作路径下所有图片
        # self.image_array = read_directory_all_pictures(self.SystemConfig.get('working_path'))

        # for value in self.image_array:
        #     item = QListWidgetItem(self)
        #     button = CustomButton(item, value['file_name'], objectName='image_btn')
        #     self.setItemWidget(item, button)
        #     self.button_item.append(button)
        #     value['button'] = button
        #
        #     def onClick_fun():
        #         image_data = value
        #         def fun():
        #             logger.debug("选择图片按钮：路径={}, width={}, height={}",
        #                          image_data['file_path'], image_data['image'].shape[1], image_data['image'].shape[0])
        #             image_widget.show_image(image_data)
        #         return fun
        #     button.onClick_fun = onClick_fun()
        #     button.clicked.connect(button.onClick_button)

    def add_button(self, item, button):
        self.setItemWidget(item, button)
        self.button_item.append(button)
