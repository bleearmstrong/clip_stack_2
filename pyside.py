import sys
from PySide import QtGui
import time
import pyperclip

import PySide.QtGui as qt
import PySide.QtCore as qc


class QCustomThread(qc.QThread):

    def __init__(self):
        qc.QThread.__init__(self)
        self.previous_value = ''
        self.new_value = ''

    def get_string(self):
        self.new_value = pyperclip.paste()
        if self.new_value != self.previous_value:
            self.previous_value = self.new_value
            return self.previous_value

    def run(self):
        while True:
            x = self.get_string()
            if x:
                self.emit(qc.SIGNAL('add_value(QString)'), x)
            time.sleep(0.1)


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.initUI()
        self.start()

    def clear(self, listwidget):
        listwidget.clear()

    def initUI(self):
        self.list = qt.QListWidget(self)
        self.list.setAlternatingRowColors(True)
        self.exit_button = qt.QPushButton('Exit', self)
        self.exit_button.clicked.connect(qc.QCoreApplication.instance().quit)
        self.clear_button = qt.QPushButton('Clear', self)
        self.clear_button.clicked.connect(lambda: self.clear(self.list))

        grid = qt.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.list, 1, 0, 10, 10)
        grid.addWidget(self.clear_button, 1, 11)
        grid.addWidget(self.exit_button, 2, 11)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 350)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QtGui.QIcon('web.png'))

    def start(self):
        self.thread = QCustomThread()
        self.connect(self.thread, qc.SIGNAL('add_value(QString)'), self.add_value)
        self.thread.start()

    def add_value(self, clip):

        new_item = qt.QListWidgetItem(clip)
        self.list.insertItem(0, new_item)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
