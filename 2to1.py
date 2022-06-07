import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QTextEdit
from PyQt5.QtCore import Qt, QUrl
from qt_material import apply_stylesheet

class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.addItems(links)


        else:
            event.ignore()
    def getText(self):
        return self.item(0).text()



class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(670, 500)
        self.setWindowTitle("ASC 편집기")
        self.listbox_view = ListBoxWidget(self)
        self.listbox_view2 = ListBoxWidget(self)
        self.listbox_view.setGeometry(20, 20, 300, 300)
        self.listbox_view2.setGeometry(350, 20, 300, 300)
        self.textedit = QTextEdit(self)
        self.textedit.setGeometry(30, 380, 300, 40)
        self.textedit.setText("Z:\\02.Work")
        self.btn = QPushButton('변환하기', self)
        self.btn.setGeometry(400, 360, 200, 40)

        self.btn2 = QPushButton('초기화', self)
        self.btn2.setGeometry(400, 410, 200, 40)
        self.btn.clicked.connect(lambda: print(self.btn_edit()))
        self.btn2.clicked.connect(lambda: print(self.btn_init()))
        self.statusBar().showMessage("준비.")

    def btn_init(self):
        self.statusBar().showMessage("준비.")
        self.listbox_view.clear()
        self.listbox_view2.clear()


    def btn_edit(self):
        try:
            file1path = self.listbox_view.getText()
            file2path = self.listbox_view2.getText()
            if file2path.lower().endswith("part.asc"):
                file1path, file2path = file2path, file1path

            f1 = open(file1path, "r")
            f2 = open(file2path, "r")
            String = []
            f_save = open(self.textedit.toPlainText() + "\\Default.asc", "w")
            f_save.write("!PADS-POWERPCB-V9.0-METRIC! NETLIST FILE FROM PADS LOGIC VVX.2.6\n*PART*       ITEMS\n")
            while True:
                line = f1.readline()
                # write at f_save if line starts with "*PART" before line start with "*"
                if line.startswith("*PART"):
                    line = f1.readline()
                    while not line.startswith("*"):
                        f_save.write(line)
                        line = f1.readline()
                if line.startswith("*NET"):
                    while not line.startswith("*END"):
                        f_save.write(line)
                        line = f1.readline()

                if not line:
                    break

                print(line)
                if not line:
                    break
            f1.close()

            f_save.write("\n*MISC*      MISCELLANEOUS PARAMETERS\n")

            while True:
                line = f2.readline()
                if line.startswith("*PART"):
                    line = f2.readline()
                    while not line.startswith("*"):
                        try:
                            String.append(line.split()[0])
                            String.append(line.split()[1])

                        except:
                            self.statusBar().showMessage("오류 발생.")
                        line = f2.readline()
                if not line:
                    break
            f_save.write("\nATTRIBUTE VALUES\n{\n")
            try:
                for i in range(0, len(String), 2):
                    f_save.write("PART {} \n".format(String[i]))
                    f_save.write("{\n")
                    f_save.write("\"Value\" {} \n".format(String[i + 1]))
                    f_save.write("}\n")
            except:
                self.statusBar().showMessage("오류 발생.")

            f_save.write("}\n")
            f_save.write("\n*END*     OF ASCII OUTPUT FILE\n")
            f_save.close()
            self.statusBar().showMessage("완료.")
        except:
            self.statusBar().showMessage("오류 발생.")






if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    apply_stylesheet(app, theme="light_blue.xml", invert_secondary=True)
    sys.exit(app.exec_())