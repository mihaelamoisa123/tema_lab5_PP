import sys
import os
import socket
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLineEdit, 
                             QTextEdit, QFileDialog, QMessageBox, QVBoxLayout, 
                             QHBoxLayout, QWidget)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class ConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text to HTML Converter")
        self.resize(600, 400)

        # Creăm interfața direct din cod ca să fim sigure că arată bine
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Rândul 1: Cale fișier + Browse
        path_layout = QHBoxLayout()
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Cale fișier...")
        self.btn_browse = QPushButton("Browse")
        path_layout.addWidget(self.input_path)
        path_layout.addWidget(self.btn_browse)
        main_layout.addLayout(path_layout)

        # Rândul 2: Zona de text + Butoane în dreapta
        content_layout = QHBoxLayout()
        self.text_result = QTextEdit()
        self.text_result.setPlaceholderText("Rezultat HTML aici...")
        
        buttons_side_layout = QVBoxLayout()
        self.btn_convert = QPushButton("Convert to HTML")
        self.btn_send = QPushButton("Send to C program")
        buttons_side_layout.addWidget(self.btn_convert)
        buttons_side_layout.addWidget(self.btn_send)
        buttons_side_layout.addStretch() # Împinge butoanele sus

        content_layout.addWidget(self.text_result)
        content_layout.addLayout(buttons_side_layout)
        main_layout.addLayout(content_layout)

        # Conectare funcții
        self.btn_browse.clicked.connect(self.choose_file)
        self.btn_convert.clicked.connect(self.process_to_html)
        self.btn_send.clicked.connect(self.send_to_c)

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Text File", "", "Text Files (*.txt)")
        if file_path: self.input_path.setText(file_path)

    def process_to_html(self):
        path = self.input_path.text()
        if not os.path.exists(path):
            QMessageBox.warning(self, "Eroare", "Selectați un fișier valid!")
            return
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        html = "<html>\n<body>\n"
        for i, line in enumerate(lines):
            clean = line.strip()
            if not clean: continue
            html += f"  <h1>{clean}</h1>\n" if i == 0 else f"  <p>{clean}</p>\n"
        html += "</body>\n</html>"
        self.text_result.setPlainText(html)

    def send_to_c(self):
        content = self.text_result.toPlainText()
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("127.0.0.1", 12345))
            client.sendall(content.encode('utf-8'))
            client.close()
            QMessageBox.information(self, "Succes", "Trimis către validatorul C!")
        except:
            QMessageBox.critical(self, "Eroare", "Porniți validator.exe mai întâi!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec())