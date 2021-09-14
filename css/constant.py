# -*- coding: utf-8 -*-
class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, 'r',  encoding='UTF-8') as file:
            return file.read()


APK_ICON_HEIGHT = 96
APK_ICON_WIDTH = 96
