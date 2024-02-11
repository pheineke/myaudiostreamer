import pytube
import pyaudio
import socket
import threading

def download_audio(youtube_url):
    yt = pytube.YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    return audio_stream.download()

def send_audio(connection, audio_file):
    CHUNK = 1024
    with open(audio_file, 'rb') as f:
        data = f.read(CHUNK)
        while data:
            connection.send(data)
            data = f.read(CHUNK)

def handle_client(client_socket):
    youtube_url = client_socket.recv(1024).decode()
    audio_file = download_audio(youtube_url)
    send_audio(client_socket, audio_file)
    client_socket.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345
    start_server(HOST, PORT)
