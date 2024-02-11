from pytube import YouTube

def downloader(url, filename):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()

