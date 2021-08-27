from gui import MainUI
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