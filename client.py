import pyaudio
import socket

def play_audio(data):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)
    stream.write(data)
    stream.close()
    audio.terminate()

def receive_audio(host, port):
    BUFFER_SIZE = 1024
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server")

    youtube_url = input("Enter YouTube URL: ")
    client_socket.send(youtube_url.encode())

    audio_data = b""
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        audio_data += data

    print("Audio received")
    play_audio(audio_data)

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345
    receive_audio(HOST, PORT)
