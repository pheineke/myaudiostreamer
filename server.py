import socket
import pyaudio
import requests
import threading
import queue

def play_audio(url_queue):
    p = pyaudio.PyAudio()

    while True:
        if not url_queue.empty():
            url = url_queue.get()
            r = requests.get(url, stream=True)
            with p.open(format=p.get_format_from_width(2), channels=2, rate=44100, output=True) as stream:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        stream.write(chunk)
            url_queue.task_done()

def start_server():
    HOST = 'localhost'  # Server-IP-Adresse
    PORT = 12345        # Port, auf dem der Server lauscht

    url_queue = queue.Queue()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print("Server gestartet...")

        threading.Thread(target=play_audio, args=(url_queue,), daemon=True).start()

        while True:
            conn, addr = s.accept()
            with conn:
                print('Verbunden mit', addr)
                data = conn.recv(1024)
                if not data:
                    break
                url = data.decode()
                print("YouTube-Video-URL empfangen:", url)
                url_queue.put(url)

start_server()
