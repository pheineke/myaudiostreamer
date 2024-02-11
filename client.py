import socket

def send_video_url_to_server(url):
    HOST = 'localhost'  # Server-IP-Adresse
    PORT = 12345        # Port, auf dem der Server lauscht

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(url.encode())

while True:
    url = input("Bitte geben Sie eine YouTube-Video-URL ein (oder Enter zum Beenden): ")
    if not url:
        break
    send_video_url_to_server(url)
