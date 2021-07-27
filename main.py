from gui.main_ui import MainUI
from PyQt5.QtWidgets import QApplication
import sys


app = QApplication(sys.argv)
myWin = MainUI()
myWin.show()
sys.exit(app.exec_())

# QTextBrowser, append(text)

