import socket
import threading
from PySide6.QtCore import QObject, Signal

class ComunicareJoc(QObject):
    mesaj_primit = Signal(str)

    def __init__(self, port_ascultare, port_destinatie):
        super().__init__()
        self.port_ascultare = port_ascultare
        self.port_destinatie = port_destinatie
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', self.port_ascultare))
        
        threading.Thread(target=self.asculta, daemon=True).start()

    def asculta(self):
        while True:
            try:
                data, _ = self.sock.recvfrom(1024)
                mesaj = data.decode()
                self.mesaj_primit.emit(mesaj)
            except:
                break

    def trimite(self, mesaj):
        self.sock.sendto(mesaj.encode(), ('127.0.0.1', self.port_destinatie))