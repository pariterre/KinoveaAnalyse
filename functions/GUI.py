import os
import sys
import glob

from PyQt5.QtWidgets import QPushButton, QApplication
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QLineEdit, QMessageBox, QRadioButton
from PyQt5.QtWidgets import QFileDialog


class InfoPopup(QWidget):
    def __init__(self):
        super().__init__()

        # Initialization of output variables
        self.mass = -1
        self.xml_file = []
        self.model = None

        grid_info = QGridLayout()  # Col 1 = labels, 2 = Edits, 3 = buttons

        # Information
        grid_info.addWidget(QLabel("Mass:"), 0, 0)
        self.mass_text = QLineEdit()
        grid_info.addWidget(self.mass_text, 0, 1)

        grid_info.addWidget(QLabel("Kinovea file:"), 2, 0)
        self.kinovea_text_empty = "No file selected"
        self.kinovea_text = QLineEdit(self.kinovea_text_empty)
        grid_info.addWidget(self.kinovea_text, 2, 1)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.click_browse)
        grid_info.addWidget(browse_button, 2, 2)

        grid_info.addWidget(QLabel("Model:"), 3, 0)
        radio_model_layou = QVBoxLayout()
        all_models = [os.path.splitext(os.path.split(f)[1])[0] for f in glob.glob("models/*.py")]
        self.radio_model = []
        for model in all_models:
            self.radio_model.append(QRadioButton(model))
            radio_model_layou.addWidget(self.radio_model[-1])
        self.radio_model[0].setChecked(True)
        grid_info.addLayout(radio_model_layou, 3, 1, 1, 2)

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

        if self.kinovea_text.text() == self.kinovea_text_empty:
            warning = QMessageBox(QMessageBox.Warning,
                                  "Choose a valid file", "Please choose a valid XML file exported by Kinovea")
            warning.exec()
            return
        self.xml_file = self.kinovea_text.text()

        for model in self.radio_model:
            if model.isChecked():
                self.model = model.text()
                break

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
    return ex.mass, ex.xml_file, ex.model


def wrong_frame(number_of_frames_max, request_frame):
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(f"You asked for the frame {request_frame}, but the trial has {number_of_frames_max} in total.")
    msg.setWindowTitle("Wrong number of frames")
    msg.show()
    app.exec_()
    exit(1)
