
class Repository:
    def __init__(self, path: str):

        if not path:
            raise ValueError("Repository path boş olamaz")

        self.path = path
        self.branches = {}
        self.current_branch = "main"

        self.branches["main"] = []
