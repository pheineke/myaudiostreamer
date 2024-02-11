import youtube_dl
import pyaudio
import socket
import threading
import os

def download_audio(youtube_url):
    ydl_opts = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        audio_file = ydl.prepare_filename(info)
    return audio_file

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
    os.remove(audio_file)
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
