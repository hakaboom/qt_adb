from gui import MainUI
from PyQt5.QtWidgets import QApplication
import sys
from css.constant import QSSLoader

app = QApplication(sys.argv)
myWin = MainUI()

myWin.show()
sys.exit(app.exec_())

