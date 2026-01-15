
class Branch:
    def __init__(self, name: str, base: str = "main"):
        if not name:
            raise ValueError("Branch adı boş olamaz")

        if " " in name:
            raise ValueError("Branch adı boşluk içeremez")

        self.name = name
        self.base = base
        self.commits = []
