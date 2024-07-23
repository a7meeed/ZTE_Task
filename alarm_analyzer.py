import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
import zipfile
import os
import pandas as pd
from openpyxl import load_workbook
from PyQt5.QtCore import Qt

class AlarmAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Alarm Analyzer')
        self.setGeometry(100, 100, 800, 600)

        # Set background image
        self.label = QLabel(self)
        pixmap = QPixmap('zte_logo.jpeg')
        self.label.setPixmap(pixmap)
        self.label.setGeometry(0, 0, 800, 600)
        self.label.setScaledContents(True)

        # Add button to upload zip file
        self.button = QPushButton('Upload Zip File', self)
        self.button.setGeometry(300, 500, 200, 50)
        self.button.clicked.connect(self.upload_zip)

    def upload_zip(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Zip File", "", "Zip Files (*.zip);;All Files (*)", options=options)
        if file_path:
            self.extract_and_analyze(file_path)

    def extract_and_analyze(self, zip_path):
        extract_dir = 'extracted_files'
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        alarm_data = []

        for file_name in os.listdir(extract_dir):
            if file_name.endswith('.xlsx'):
                file_path = os.path.join(extract_dir, file_name)
                df = pd.read_excel(file_path)
                alarm_data.append(df)

        self.classify_alarms(alarm_data)
        
        QMessageBox.information(self, 'Success', 'Alarms have been classified and saved.')

    def classify_alarms(self, dataframes):
        combined_df = pd.concat(dataframes)
        alarm_groups = combined_df.groupby('Alarm Code')

        output_dir = 'classified_alarms'
        os.makedirs(output_dir, exist_ok=True)

        for alarm_code, group in alarm_groups:
            output_file = os.path.join(output_dir, f'{alarm_code}_alarms.xlsx')
            group.to_excel(output_file, index=False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    analyzer = AlarmAnalyzer()
    analyzer.show()
    sys.exit(app.exec_())
