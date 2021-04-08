import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.host = 'localhost'
        self.port = 25570
        self.addr = (self.host, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return True

        except ConnectionRefusedError:
            print('[ERROR] An error occured while trying to connect to the server!')
            return False

    def disconnect(self):
        self.client.close()

