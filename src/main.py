from PyQt5.QtWidgets import QApplication
import sys
from gui.main_window import *

def main(argv):
    app = QApplication(argv)
    window = MainWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main(sys.argv)