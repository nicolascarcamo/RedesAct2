import socket
import sys

class socketTCP():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        #Use UDP Socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))

    def send(self, data):
        self.socket.send(data)

    def recv(self):
        try:
            data = self.socket.recv(1024)
            return data
        except:
            return None

    def close(self):
        self.socket.close()