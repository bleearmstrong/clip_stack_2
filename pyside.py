import sys
from PySide import QtGui
import time
import pyperclip
import os

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

    def clear_item(self):
        item = self.list.selectedItems()
        self.list.takeItem(self.list.row(item[0]))

    def clear_list(self, listwidget):
        listwidget.clear()

    def return_value(self, index):
        pyperclip.copy(self.list.currentItem().text())

    def save(self):
        save_path = os.path.join(os.getcwd()
                                 , 'stack.txt')
        save_path = qt.QFileDialog.getSaveFileName(self
                                                   , 'Save Stack'
                                                   , save_path
                                                   , 'stack.txt')
        if len(save_path[0]) > 0:
            with open(save_path[0], 'w') as save_file:
                for i in range(self.list.count()):
                    save_file.write(str(self.list.item(i).text()))
                    save_file.write('\n<<entry_delimiter>>\n')

    def initUI(self):
        self.list = qt.QListWidget(self)
        self.list.setAlternatingRowColors(True)
        self.list.setStyleSheet("alternate-background-color: grey;"
                                "background-color: white;"
                                "color: black;"
                                )
        self.list.clicked.connect(self.return_value)
        self.exit_button = qt.QPushButton('Exit', self)
        self.exit_button.clicked.connect(qc.QCoreApplication.instance().quit)
        self.clear_item_button = qt.QPushButton('Clear Item', self)
        self.clear_item_button.clicked.connect(self.clear_item)
        self.clear_list_button = qt.QPushButton('Clear List', self)
        self.clear_list_button.clicked.connect(lambda: self.clear_list(self.list))
        self.save_button = qt.QPushButton('Save List', self)
        self.save_button.clicked.connect(self.save)

        grid = qt.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.list, 1, 0, 10, 10)
        grid.addWidget(self.clear_item_button, 1, 11)
        grid.addWidget(self.clear_list_button, 2, 11)
        grid.addWidget(self.exit_button, 3, 11)
        grid.addWidget(self.save_button, 4, 11)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 350)
        self.setWindowTitle('Clip_Stack')
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
