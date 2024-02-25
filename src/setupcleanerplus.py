import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QComboBox, QVBoxLayout, \
    QMessageBox, QSlider
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.curDirectory = ""
        self.selectedExtensions = []
        self.init_ui()

    def init_ui(self):
        # Create widgets
        fileDirButton = QPushButton("Select File Directory", self)
        fileDirButton.move(20, 20)
        fileDirButton.resize(150, 50)

        self.fileDirLabel = QLabel("No directory selected", self)
        self.fileDirLabel.resize(1000, 10)
        self.fileDirLabel.move(30, 80)

        self.text_selExt = QLabel("Select File Extension", self)
        self.text_selExt.move(200, 20)

        extSelectBox = QComboBox(self)
        extSelectBox.addItems(["Installation/Setup Files", ".zip", ".rar", ".png", ".jpg", ".jpeg", ".gif",
                               ".bmp", ".tiff", ".tif", ".webp", ".mp4", ".mkv", ".avi", ".mov", ".wmv",
                               ".flv", ".webm", ".mp3", ".wav", ".flac", ".ogg", ".wma", ".aac", ".m4a",
                               ".opus", ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".txt",
                               ".html", ".css", ".js"])
        extSelectBox.setGeometry(200, 40, 150, 20)

        refreshButton = QPushButton("Refresh List", self)
        refreshButton.setGeometry(400, 40, 100, 20)

        deleteButton = QPushButton("Delete Selected Files", self)
        deleteButton.setGeometry(520, 40, 150, 20)

        self.fileListLabel = QLabel(self)
        self.fileListLabel.setGeometry(30, 120, 600, 620)
        self.fileListLabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        sliderLabel = QLabel("Select Date Range:", self)
        sliderLabel.setGeometry(30, 750, 150, 20)

        self.dateSlider = QSlider(Qt.Horizontal, self)
        self.dateSlider.setGeometry(200, 750, 400, 20)
        self.dateSlider.setMinimum(0)
        self.dateSlider.setMaximum(365)  # Number of days in a year
        self.dateSlider.setValue(365)

        self.dateLabel = QLabel("Newer                                                                                                                 Older", self)
        self.dateLabel.move(200, 770)

        sizeLabel = QLabel("Combined Size: 0 MB", self)
        sizeLabel.setGeometry(30, 90, 150, 20)
        sizeLabel.setObjectName("sizeLabel")

        logoLabel = QLabel(self)
        logoLabel.setGeometry(self.width() - 130, self.height() + 150, 180, 90)
        logo = QPixmap('scpLogo.png')
        logoLabel.setPixmap(logo)
        logoLabel.setScaledContents(True)

        # Connect signals and slots
        fileDirButton.clicked.connect(self.selectFileDir)
        extSelectBox.currentIndexChanged.connect(self.updateSelectedExtensions)
        refreshButton.clicked.connect(self.refreshFileList)
        deleteButton.clicked.connect(self.deleteSelectedFiles)
        self.dateSlider.valueChanged.connect(self.refreshFileList)

        # Style Sheet
        self.setStyleSheet("""
            QWidget {
                background-color: black;
                color: white;
            }

            QPushButton, QComboBox {
                border: 2px solid #0078FF;
                background-color: black;
                color: white;
            }
        """)

        # Set window properties
        self.setWindowTitle("SetupCleanerPlus")
        self.setGeometry(100, 100, 700, 800)
        self.show()

    def selectFileDir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", "C:\\", QFileDialog.ShowDirsOnly)
        self.curDirectory = directory
        self.fileDirLabel.setText(str(self.curDirectory))
        self.refreshFileList()

    def updateSelectedExtensions(self, index):
        selected_text = self.sender().currentText()
        if selected_text == "Installation/Setup Files":
            self.selectedExtensions = ['setup', 'installer', '.msi', '.msm', '.msp', '.mst', '.msu', '.idt', '.cub', '.pcp', "-x64", "-x86", "-amd64", "-x32", "-amd32", "-win64", "-64-bit",  "-32-bit", ".exe"]
        else:
            self.selectedExtensions = [selected_text]
        self.refreshFileList()


    def refreshFileList(self):
        if not self.curDirectory:
            return

        selected_date_range = self.dateSlider.value()
        files = [f for f in os.listdir(self.curDirectory) if any(ext.lower() in f.lower() for ext in self.selectedExtensions)]
        file_paths = [os.path.join(self.curDirectory, f) for f in files if os.path.isfile(os.path.join(self.curDirectory, f))]

        self.fileListLabel.setText("\n".join(files[:selected_date_range]))

        try:
            # Calculate the combined size of selected files
            total_size = sum(os.path.getsize(f) for f in file_paths[:selected_date_range])
            total_size_mb = total_size / (1024 * 1024)  # Convert to megabytes
            sizeLabel = self.findChild(QLabel, 'sizeLabel')  # Retrieve the size label
            sizeLabel.setText(f"Combined Size: {total_size_mb:.2f} MB")
        except (PermissionError, FileNotFoundError) as e:
            print(f"Error calculating file size: {e}")
            sizeLabel = self.findChild(QLabel, 'sizeLabel')
            sizeLabel.setText("Combined Size: N/A")



    def deleteSelectedFiles(self):
        reply = QMessageBox.question(self, 'Delete Files', 'Are you sure you want to delete the selected files?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for file_name in os.listdir(self.curDirectory):
                if file_name.endswith(tuple(self.selectedExtensions)):
                    file_path = os.path.join(self.curDirectory, file_name)
                    os.remove(file_path)
            self.refreshFileList()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
