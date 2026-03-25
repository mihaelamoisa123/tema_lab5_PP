import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QGridLayout, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt
import database
from comunicare import ComunicareJoc

class JocXsiO(QMainWindow):
    def __init__(self, port_meu, port_el, simbol):
        super().__init__()
        self.setWindowTitle(f"Joc X si O - Jucator {simbol}")
        self.setFixedSize(400, 500)
        database.init_db()
        
        self.simbol = simbol
        self.randul_meu = (simbol == "X")
        self.port_meu = port_meu
        self.port_el = port_el
        self.nume_adversar = "Adversar"
        self.nume_meu = "Anonim"

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        top_layout = QHBoxLayout()
        self.input_nume = QLineEdit()
        self.input_nume.setPlaceholderText("Introdu numele tau...")
        self.btn_start = QPushButton("Start Joc")
        self.btn_start.clicked.connect(self.trimite_nume)
        top_layout.addWidget(self.input_nume)
        top_layout.addWidget(self.btn_start)
        main_layout.addLayout(top_layout)

        self.lbl_score = QLabel("Scor: 0 - 0")
        self.lbl_score.setAlignment(Qt.AlignCenter)
        self.lbl_status = QLabel(f"Esti {self.simbol}. Asteptam conexiunea...")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.lbl_score)
        main_layout.addWidget(self.lbl_status)

        grid_container = QWidget()
        self.grid_logic = QGridLayout(grid_container)
        self.butoane = []
        for i in range(9):
            btn = QPushButton("")
            btn.setFixedSize(100, 100)
            btn.setStyleSheet("font-size: 30px; font-weight: bold; background-color: #f0f0f0;")
            btn.clicked.connect(lambda ch=None, idx=i: self.apasat_buton(idx))
            self.grid_logic.addWidget(btn, i // 3, i % 3)
            self.butoane.append(btn)
        main_layout.addWidget(grid_container)

        self.com = ComunicareJoc(self.port_meu, self.port_el)
        self.com.mesaj_primit.connect(self.primeste_mesaj)

    def trimite_nume(self):
        self.nume_meu = self.input_nume.text() if self.input_nume.text() else "Player"
        self.com.trimite(f"HELLO:{self.nume_meu}")
        self.btn_start.setEnabled(False)
        self.btn_start.setText("Conectat")

    def apasat_buton(self, idx):
        if self.randul_meu and self.butoane[idx].text() == "":
            self.butoane[idx].setText(self.simbol)
            self.butoane[idx].setStyleSheet(f"font-size: 30px; font-weight: bold; color: {'red' if self.simbol == 'X' else 'blue'};")
            self.com.trimite(f"MOVE:{idx}")
            self.randul_meu = False
            self.lbl_status.setText("Asteapta adversarul...")
            self.verifica_final()

    def primeste_mesaj(self, mesaj):
        if mesaj.startswith("HELLO:"):
            self.nume_adversar = mesaj.split(":")[1]
            s1, s2 = database.get_score(self.nume_meu, self.nume_adversar)
            self.lbl_score.setText(f"Scor: {s1} - {s2}")
            self.lbl_status.setText(f"Joci contra: {self.nume_adversar}")
            
        elif mesaj.startswith("MOVE:"):
            idx = int(mesaj.split(":")[1])
            adv = "O" if self.simbol == "X" else "X"
            self.butoane[idx].setText(adv)
            self.butoane[idx].setStyleSheet(f"font-size: 30px; font-weight: bold; color: {'blue' if adv == 'O' else 'red'};")
            self.randul_meu = True
            self.lbl_status.setText("Randul tau!")
            self.verifica_final()

    def verifica_final(self):
        b = [btn.text() for btn in self.butoane]
        linii = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        
        for l in linii:
            if b[l[0]] == b[l[1]] == b[l[2]] != "":
                castigator = b[l[0]]
                if castigator == self.simbol:
                    database.update_score(self.nume_meu, self.nume_adversar, self.nume_meu)
                    QMessageBox.information(self, "Final", "Ai castigat!")
                else:
                    QMessageBox.information(self, "Final", f"A castigat {self.nume_adversar}!")
                
                self.actualizeaza_scor_vizual()
                self.reseteaza()
                return

        if "" not in b:
            QMessageBox.information(self, "Final", "Remiza!")
            self.reseteaza()

    def actualizeaza_scor_vizual(self):
        s1, s2 = database.get_score(self.nume_meu, self.nume_adversar)
        self.lbl_score.setText(f"Scor: {s1} - {s2}")

    def reseteaza(self):
        for btn in self.butoane: 
            btn.setText("")
            btn.setStyleSheet("font-size: 30px; font-weight: bold; background-color: #f0f0f0;")
        self.randul_meu = (self.simbol == "X")
        self.lbl_status.setText("Randul tau!" if self.randul_meu else "Asteapta adversarul...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        window = JocXsiO(5006, 5005, "O")
    else:
        window = JocXsiO(5005, 5006, "X")
    window.show()
    sys.exit(app.exec())