import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QTextEdit, QPushButton, QLabel)
from multiprocessing import Process, Queue
import procesare_numere 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interfață grafică - Lab 5")
        self.resize(600, 450)
        
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #2b2b2b; color: white;")
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)

        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("List of integers:"))
        self.input_list = QLineEdit("1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15")
        self.input_list.setStyleSheet("background-color: white; color: black; padding: 5px;")
        top_layout.addWidget(self.input_list)
        main_layout.addLayout(top_layout)

        self.result_area = QTextEdit()
        self.result_area.setStyleSheet("background-color: white; color: black; font-family: Consolas;")
        self.result_area.setPlaceholderText("Rezultatele vor aparea aici...")
        main_layout.addWidget(self.result_area)

        btn_layout = QHBoxLayout()
        self.btn_odd = QPushButton("Filter odd")
        self.btn_prime = QPushButton("Filter primes")
        self.btn_sum = QPushButton("Sum numbers")
        
        style = "background-color: #555; color: white; padding: 10px; border-radius: 5px;"
        self.btn_odd.setStyleSheet(style)
        self.btn_prime.setStyleSheet(style)
        self.btn_sum.setStyleSheet(style)
        
        btn_layout.addWidget(self.btn_odd)
        btn_layout.addWidget(self.btn_prime)
        btn_layout.addWidget(self.btn_sum)
        main_layout.addLayout(btn_layout)

        self.btn_odd.clicked.connect(lambda: self.run_task(procesare_numere.filter_odd_task))
        self.btn_prime.clicked.connect(lambda: self.run_task(procesare_numere.filter_prime_task))
        self.btn_sum.clicked.connect(lambda: self.run_task(procesare_numere.sum_numbers_task))

    def run_task(self, task_func):
        try:
            data = [int(x.strip()) for x in self.input_list.text().split(',')]
            q = Queue()
            p = Process(target=task_func, args=(data, q))
            p.start()
            p.join()
            if not q.empty():
                res = q.get()
                self.result_area.append(str(res))
        except Exception as e:
            self.result_area.append(f"Eroare: Introduceti numere valide! ({e})")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
