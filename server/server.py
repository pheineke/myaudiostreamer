import socket
import threading
#############
from message import Message
#############

def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

class Server:
    def __init__(self) -> None:
        self.host = get_ip()
        self.port = 5555
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def inputlistener(self):
        while True: 
            userinput = Message(input("["))
            self.server.sendall(userinput)

    def messagelistener(self):
        while True:
            data = Message(self.server.recv(1024))
            print(data.content_decode())
            

    def main(self):
        self.server.listen()
        
        queue_thread = threading.Thread(target=lambda: self.messagelistener)
        queue_thread.daemon = True
        queue_thread.start()
        
        
        


if __name__ == "__main__":
    s = Server()
    s.main()