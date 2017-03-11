import sys
from PySide import QtGui
import time
import pyperclip

import PySide.QtGui as qt
import PySide.QtCore as qc


class QCustomThread(qc.QThread):


    def __init__(self):
        # super(QCustomThread, self).__init__()
        qc.QThread.__init__(self)
        self.previous_value = ''
        self.new_value = ''

    def get_string(self):
        self.new_value = pyperclip.paste()
        if self.new_value != self.previous_value:
            self.previous_value = self.new_value
            print(self.previous_value)
            return self.previous_value

    def run(self):
        print('running')
        while True:
            x = self.get_string()
            print('running')
            if x:
                self.emit(qc.SIGNAL('add_value(QString)'), x)
            time.sleep(0.1)


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.list = qt.QListWidget(self)
        self.initUI()
        self.start()

    def initUI(self):
        print('initUI')
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QtGui.QIcon('web.png'))

    def start(self):
        print('start')
        self.thread = QCustomThread()
        self.connect(self.thread, qc.SIGNAL('add_value(QString)'), self.add_value)
        self.thread.start()

    def add_value(self, clip):

        new_item = qt.QListWidgetItem(clip)
        self.list.addItem(new_item)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
