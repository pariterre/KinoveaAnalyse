import sys
from PyQt5.QtWidgets import QPushButton, QApplication
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QFileDialog


class InfoPopup(QWidget):
    def __init__(self):
        super().__init__()

        # Initialization of output variables
        self.mass = -1
        self.time_index = -1
        self.xml_file = []

        grid_info = QGridLayout()  # Col 1 = labels, 2 = Edits, 3 = buttons

        # Information
        grid_info.addWidget(QLabel("Mass:"), 0, 0)
        self.mass_text = QLineEdit()
        grid_info.addWidget(self.mass_text, 0, 1)

        grid_info.addWidget(QLabel("Time index:"), 1, 0)
        self.time_index_text = QLineEdit()
        grid_info.addWidget(self.time_index_text, 1, 1)

        grid_info.addWidget(QLabel("Kinovea file:"), 2, 0)
        self.kinovea_text_empty = "No file selected"
        self.kinovea_text = QLineEdit(self.kinovea_text_empty)
        grid_info.addWidget(self.kinovea_text, 2, 1)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.click_browse)
        grid_info.addWidget(browse_button, 2, 2)

        # Finish button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.click_method)
        self.from_ok = False

        hbox_finalize = QHBoxLayout()
        hbox_finalize.addStretch(1)
        hbox_finalize.addWidget(ok_button)
        hbox_finalize.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(grid_info)
        vbox.addLayout(hbox_finalize)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Subject informations')
        self.show()

    def click_method(self):
        try:
            self.mass = float(self.mass_text.text())
        except ValueError:
            warning = QMessageBox(QMessageBox.Warning, "Error in mass", "Mass must be in kilogram")
            warning.exec()
            return

        try:
            self.time_index = int(self.time_index_text.text())
            if self.time_index < 0:
                self.time_index
                raise ValueError
        except ValueError:
            warning = QMessageBox(QMessageBox.Warning, "Error in time index", "Time index must be a positive integer")
            warning.exec()
            return

        if self.kinovea_text.text() == self.kinovea_text_empty:
            warning = QMessageBox(QMessageBox.Warning,
                                  "Choose a valid file", "Please choose a valid XML file exported by Kinovea")
            warning.exec()
            return
        self.xml_file = self.kinovea_text.text()

        self.from_ok = True
        self.close()

    def closeEvent(self, event):
        self.click_cancel()

    def click_cancel(self):
        if not self.from_ok:
            exit(0)

    def click_browse(self):
        file = QFileDialog.getOpenFileName(filter='*.xml')
        if not file:
            self.kinovea_text.setText(self.kinovea_text_empty)
        else:
            self.kinovea_text.setText(file[0])


def get_info():
    app = QApplication(sys.argv)
    ex = InfoPopup()
    app.exec_()
    return ex.mass, ex.time_index, ex.xml_file
