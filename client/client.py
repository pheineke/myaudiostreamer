import socket
import threading
#############
from message import Message
#############

def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

class Client:
    def __init__(self) -> None:
        self.host = get_ip()
        self.port = 5555
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def inputlistener(self):
        while True: 
            userinput = input("[")
            self.server.sendall(userinput.encode())

    def messagelistener(self):
        while True:
            data = self.server.recv(1024).decode('utf-8')
            print(data)
            

    def main(self):
        self.server.listen()

        queue_thread = threading.Thread(target=lambda: self.messagelistener)
        queue_thread.daemon = True
        queue_thread.start()
        
        self.inputlistener()


if __name__ == "__main__":
    c = Client()
    c.main() 