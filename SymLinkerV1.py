import os
import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QPainter, QLinearGradient, QColor
from PyQt5.QtCore import Qt, pyqtSlot

class SymlinkCreator(QWidget):
    def __init__(self):
        super().__init__()

        self.source_files = []
        self.target_dir = ""

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.run_button = QPushButton('Run', self)
        self.select_files_button = QPushButton('Select Files', self)
        self.target_button = QPushButton('Target', self)

        self.source_text_area = QTextEdit(self)
        self.target_text_area = QTextEdit(self)

        # Set the colors of the text boxes and buttons
        self.source_text_area.setStyleSheet("background-color: #070707; color: white;")
        self.target_text_area.setStyleSheet("background-color: #070707; color: white;")
        self.run_button.setStyleSheet("background-color: #070707; color: white; border: 2px solid powderblue;")
        self.select_files_button.setStyleSheet("background-color: #070707; color: white; border: 2px solid powderblue;")
        self.target_button.setStyleSheet("background-color: #070707; color: white; border: 2px solid powderblue;")

        self.layout.addWidget(self.run_button)
        self.layout.addWidget(self.select_files_button)
        self.layout.addWidget(self.target_button)
        self.layout.addWidget(self.source_text_area)
        self.layout.addWidget(self.target_text_area)

        self.run_button.clicked.connect(self.create_symlinks)
        self.select_files_button.clicked.connect(self.select_files)
        self.target_button.clicked.connect(self.select_target)

    def paintEvent(self, event):
        painter = QPainter(self)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor.fromRgbF(random.random(), random.random(), random.random(), 1.0))
        gradient.setColorAt(1.0, QColor.fromRgbF(random.random(), random.random(), random.random(), 1.0))

        painter.setBrush(gradient)
        painter.drawRect(0, 0, self.width(), self.height())

    def select_files(self):
        self.source_files = QFileDialog.getOpenFileNames(self, 'Select Files')[0]
        # Display selected files in the text area
        self.source_text_area.setText("\n".join(self.source_files))

    def select_target(self):
        self.target_dir = QFileDialog.getExistingDirectory(self, 'Select Target Directory')
        # Display target directory in the text area
        self.target_text_area.setText(self.target_dir)

    def create_symlinks(self):
        if not self.source_files or not self.target_dir:
            QMessageBox.critical(self, "Error", "Please select source files and a target directory.")
            return

        for source_file in self.source_files:
            filename = os.path.basename(source_file)
            target_file = os.path.join(self.target_dir, filename)
            try:
                os.symlink(source_file, target_file)
            except OSError as e:
                QMessageBox.critical(self, "Error", f"Failed to create symlink: {e}")
                return

        QMessageBox.information(self, "Done!", "Symbolic links created successfully.")

        # Clear settings and restart
        self.source_files = []
        self.target_dir = ""
        self.source_text_area.clear()
        self.target_text_area.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = SymlinkCreator()
    window.show()

    sys.exit(app.exec_())
