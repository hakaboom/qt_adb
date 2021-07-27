from gui.main_ui import MainUI
from PyQt5.QtWidgets import QApplication
import sys
from css.constant import QSSLoader

style_file = './css/style_test.qss'
style_sheet = QSSLoader.read_qss_file(style_file)

app = QApplication(sys.argv)
myWin = MainUI()
myWin.setStyleSheet(style_sheet)

myWin.show()
sys.exit(app.exec_())

# QTextBrowser, append(text)

# https://github.com/hustlei/QssStylesheetEditor/blob/e1a145dcd9028893b33ef5c5ae11d82ad02f1b9a/src/ui/preview.py#L182