import sys
from PySide import QtGui
import time
import pyperclip
import os
import re

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
            with open(save_path[0], 'wb') as save_file:
                for i in range(self.list.count()):
                    save_file.write(bytes(self.list.item(i).text(), 'UTF-8'))
                    save_file.write(b'\n<<entry_delimiter>>\n')

    def read_lines_delimiter(self, f, delim):
        buf = ''
        while True:
            while delim in buf:
                pos = buf.index(delim)
                yield buf[:pos]
                buf = buf[pos + len(delim):]
            chunk = f.read(4096).decode('UTF-8')
            if not chunk:
                yield buf
                break
            buf += chunk

    def single_strip(self, line):
        regex = r"\n?(.+)\n"
        try:
            matches = re.search(regex, line, re.DOTALL)
            return matches.group(1)
        except:
            pass


    def load(self):
        load_path = os.getcwd()
        load_path = qt.QFileDialog.getOpenFileName(self
                                                   , 'Open Stack'
                                                   , load_path)
        if len(load_path[0]) > 0:
            self.list.clear()
            new_list = list()
            with open(load_path[0], 'rb') as load_file:
                for line in self.read_lines_delimiter(load_file, '<<entry_delimiter>>'):
                    if line.strip() != '':
                        new_list.append(line)
                for line in reversed(new_list):
                    new_item = qt.QListWidgetItem(self.single_strip(line))
                    self.list.insertItem(0, new_item)

    def insert_stack(self):
        insert_path = os.getcwd()
        insert_path = qt.QFileDialog.getOpenFileName(self
                                                     , 'Open Stack'
                                                     , insert_path)
        if len(insert_path[0]) > 0:
            new_list = list()
            with open(insert_path[0], 'rb') as insert_file:
                for line in self.read_lines_delimiter(insert_file, '<<entry_delimiter>>'):
                    if line.strip() != '':
                        new_list.append(line)
                for item in reversed(new_list):
                    new_item = qt.QListWidgetItem(self.single_strip(item))
                    self.list.insertItem(0, new_item)


    def use_search(self):
        if self.search_box.text().strip() == '':
            self.stacked.setCurrentWidget(self.list)
        else:

            filtered_list = list()
            print(self.search_box.text())
            for index in range(self.list.count()):
                print(self.list.item(index).text())

                if self.search_box.text() in str(self.list.item(index).text()):
                    filtered_list.append(self.list.item(index))
            self.f_list.clear()
            print(str(filtered_list[0].text()))
            # self.f_list.insertItems(0, filtered_list)
            for i, item in enumerate(filtered_list):
                new_item = qt.QListWidgetItem(item)
                # self.list.insertItem(0, new_item)
                self.f_list.insertItem(i, new_item)
            self.stacked.setCurrentWidget(self.f_list)

    def initUI(self):
        self.list = qt.QListWidget(self)
        self.list.setAlternatingRowColors(True)
        self.list.setStyleSheet("alternate-background-color: grey;"
                                "background-color: white;"
                                "color: black;"
                                )
        self.f_list = qt.QListWidget(self)
        self.f_list.setAlternatingRowColors(True)
        self.f_list.setStyleSheet("alternate-background-color: grey;"
                                "background-color: white;"
                                "color: black;"
                                )
        self.list.clicked.connect(self.return_value)
        self.stacked = qt.QStackedWidget(self)
        self.stacked.addWidget(self.f_list)
        self.stacked.addWidget(self.list)
        self.stacked.setCurrentWidget(self.list)
        self.exit_button = qt.QPushButton('Exit', self)
        self.exit_button.clicked.connect(qc.QCoreApplication.instance().quit)
        self.clear_item_button = qt.QPushButton('Clear Item', self)
        self.clear_item_button.clicked.connect(self.clear_item)
        self.clear_list_button = qt.QPushButton('Clear Stack', self)
        self.clear_list_button.clicked.connect(lambda: self.clear_list(self.list))
        self.save_button = qt.QPushButton('Save Stack', self)
        self.save_button.clicked.connect(self.save)
        self.load_button = qt.QPushButton('Load Stack', self)
        self.load_button.clicked.connect(self.load)
        self.insert_button = qt.QPushButton('Insert Stack', self)
        self.insert_button.clicked.connect(self.insert_stack)
        self.search_box = qt.QLineEdit()
        self.search_box.textChanged.connect(self.use_search)

        grid = qt.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.search_box, 1, 0, 1, 8)
        grid.addWidget(self.stacked, 2, 0, 10, 10)
        grid.addWidget(self.clear_item_button, 2, 11)
        grid.addWidget(self.clear_list_button, 3, 11)
        grid.addWidget(self.exit_button, 9, 11)
        grid.addWidget(self.save_button, 4, 11)
        grid.addWidget(self.load_button, 5, 11)
        grid.addWidget(self.insert_button, 6, 11)

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
