
class Commit:
    def __init__(self, hash: str, message: str):
        if len(message.strip()) < 3:
            raise ValueError("Commit mesajı çok kısa")

        self.hash = hash
        self.message = message
