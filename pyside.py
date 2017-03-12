import sys
from PySide import QtGui
import time
import pyperclip
import os
import re

import PySide.QtGui as qt
import PySide.QtCore as qc

#z
class QListItemSub(qt.QListWidgetItem):

    def __init__(self, item, searched):
        qt.QListWidgetItem.__init__(self, item)
        if not searched:
            self.full_text = self.text()
        else:
            self.full_text = item.full_text
        self.change_display()

    def change_display(self):
        line_counter = len(str(self.text()).split('\n'))
        if line_counter > 5:
            new_display = '\n'.join(str(self.text()).split('\n')[0:5])
            new_display += '\n...'
            self.setText(new_display)

    def change_display_search(self, regex_b, pattern):
        temp_list = self.full_text.split('\n')
        if regex_b:
            search_index = min([i for i, line in enumerate(temp_list) if re.search(pattern, line)])
        else:
            search_index = min([i for i, line in enumerate(temp_list) if pattern in line])
        new_display = '\n'.join(temp_list[max([0, search_index  - 2]):min([search_index + 3, len(temp_list)])])
        self.setText(new_display)


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

        self.use_regex_b = False
        self.initUI()
        self.start()

    def clear_item(self):
        item = self.list.selectedItems()
        self.list.takeItem(self.list.row(item[0]))

    def clear_list(self, listwidget):
        listwidget.clear()
        self.stacked.setCurrentWidget(self.list)

    def return_value(self, index):
        pyperclip.copy(self.list.currentItem().full_text)

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
                    save_file.write(bytes(self.list.item(i).full_text, 'UTF-8'))
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
                    new_item = QListItemSub(self.single_strip(line), False)
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
                    new_item = QListItemSub(self.single_strip(item), False)
                    self.list.insertItem(0, new_item)


    def use_search(self):
        if self.search_box.text().strip() == '':
            self.stacked.setCurrentWidget(self.list)
        else:
            filtered_list = list()
            for index in range(self.list.count()):
                if self.use_regex_b:
                    if re.search(str(self.search_box.text()), str(self.list.item(index).full_text)):
                        if not re.search(str(self.search_box.text()), str(self.list.item(index).text())):
                            reset_text = True
                        else:
                            reset_text = False
                        filtered_list.append((self.list.item(index), reset_text))
                else:
                    if self.search_box.text() in str(self.list.item(index).full_text):
                        if self.search_box.text() not in str(self.list.item(index).text()):
                            reset_text = True
                        else:
                            reset_text = False
                        filtered_list.append((self.list.item(index), reset_text))
            self.f_list.clear()
            if filtered_list:
                for i, item in enumerate(filtered_list):
                    new_item = QListItemSub(item[0], True)
                    if item[1]:
                        new_item.change_display_search(self.use_regex_b, str(self.search_box.text()))
                    self.f_list.insertItem(i, new_item)
            self.stacked.setCurrentWidget(self.f_list)

    def use_regex(self, state):
        if state == qc.Qt.Checked:
            self.use_regex_b = True
        else:
            self.use_regex_b = False

    def keep_filtered_list(self):
        self.list.clear()
        for i in range(self.f_list.count()):
            new_item = QListItemSub(self.f_list.item(i), False)
            self.list.insertItem(i, new_item)

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
        self.clear_item_button.clicked.connect(self.use_search)
        self.clear_list_button = qt.QPushButton('Clear Stack', self)
        self.clear_list_button.clicked.connect(lambda: self.clear_list(self.list))
        self.save_button = qt.QPushButton('Save Stack', self)
        self.save_button.clicked.connect(self.save)
        self.load_button = qt.QPushButton('Load Stack', self)
        self.load_button.clicked.connect(self.load)
        self.load_button.clicked.connect(self.use_search)
        self.insert_button = qt.QPushButton('Insert Stack', self)
        self.insert_button.clicked.connect(self.insert_stack)
        self.insert_button.clicked.connect(self.use_search)
        self.search_box = qt.QLineEdit()
        self.search_box.setPlaceholderText('Search')
        self.search_box.textChanged.connect(self.use_search)
        self.regex_box = qt.QCheckBox('Use regex', self)
        self.regex_box.stateChanged.connect(self.use_regex)
        self.regex_box.stateChanged.connect(self.use_search)
        self.keep_filtered_button = qt.QPushButton('Keep Filtered Stack', self)
        self.keep_filtered_button.clicked.connect(self.keep_filtered_list)

        grid = qt.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.search_box, 1, 0, 1, 8)
        grid.addWidget(self.regex_box, 1, 9)
        grid.addWidget(self.stacked, 2, 0, 10, 10)
        grid.addWidget(self.clear_item_button, 2, 11)
        grid.addWidget(self.clear_list_button, 3, 11)
        grid.addWidget(self.exit_button, 9, 11)
        grid.addWidget(self.save_button, 4, 11)
        grid.addWidget(self.load_button, 5, 11)
        grid.addWidget(self.insert_button, 6, 11)
        grid.addWidget(self.keep_filtered_button, 7, 11)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 350)
        self.setWindowTitle('Clip_Stack')
        self.setWindowIcon(QtGui.QIcon('web.png'))

    def start(self):
        self.thread = QCustomThread()
        self.connect(self.thread, qc.SIGNAL('add_value(QString)'), self.add_value)
        self.thread.start()

    def add_value(self, clip):
        new_item = QListItemSub(clip, False)
        self.list.insertItem(0, new_item)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
