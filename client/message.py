class Message:
    def __init__(self, content) -> None:
        self.content = content.decode()
        self.content_encode = self.content.encode()
        self.author