import sys
from gui.main_window import *

def main(argv):
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)