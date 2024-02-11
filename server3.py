import socket
import subprocess
import threading
import queue
import pyaudio
from pytube import YouTube
import os
import wave
from pydub import AudioSegment



# Queue für die zu spielenden Videos
video_queue = queue.Queue()

# Funktion zum Herunterladen und Abspielen von Videos
def download_video(url,filename):
    if os.path.exists(f"./{filename}.wav"):
        os.remove(f"./{filename}.wav")
    try: 
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        video.download(filename=f"{filename}.mp4")
        subprocess.run(f"ffmpeg -i {filename}.mp4 -ac 2 -f wav {filename}.wav", shell=True)
        if os.path.exists(f"./{filename}.mp4"):
            os.remove(f"./{filename}.mp4")
    except Exception as e:
        if "AgeRestrictedError" in e:
            print("CONTENT AGE RESTRICTED")
    

def play_video(url):
    CHUNK = 1024
    download_video(url,"video")
    # Audio abspielen
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                output=True)
    wf = wave.open("./video.wav", "rb")
    data0 = wf.readframes(CHUNK)
    while data0:
        stream.write(data0)
        data0 = wf.readframes(1024)
        if data0 is None:
            os.remove("video.wav")
    stream.stop_stream()
    stream.close()
    p.terminate()
    

# Funktion für den Client-Handler
def client_handler(conn, addr):
    print(f"Verbunden mit {addr}")

    while True:
        data = conn.recv(1024).decode('utf-8')
        print(data)
        if not data:
            print(f"{addr} hat die Verbindung getrennt.")
            break

        video_queue.put(data)
        print(f"Video von {addr} hinzugefügt: {data}")
    conn.close()

# Funktion zum Verwalten der Video-Warteschlange
def manage_queue():
    while True:
        if not video_queue.empty():
            url = video_queue.get()
            print(f"Starte Wiedergabe von: {url}")
            play_video(url)

# Hauptfunktion des Servers
def main():
    host = "10.10.10.181"
    port = 5555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Server gestartet auf {host}:{port}")

    # Thread für die Verwaltung der Warteschlange starten
    queue_thread = threading.Thread(target=manage_queue)
    queue_thread.daemon = True
    queue_thread.start()

    while True:
        x = input()
        if x == "queue":
            print(video_queue.queue)
        conn, addr = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(conn, addr))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    main()
