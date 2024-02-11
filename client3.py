import socket

def main():
    host = "10.10.10.181"
    port = 5554

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    while True:
        video_url = input("Bitte geben Sie den YouTube-Link ein (oder 'exit' zum Beenden): ")
        if video_url.lower() == 'exit':
            break
        client.sendall(video_url.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    main()
