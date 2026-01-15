from Core.libwyag import repo_find, object_find, object_read, tree_checkout
import os

class CheckoutService:

    def checkout(self, repo_path: str, commit: str, path: str):
        repo = repo_find(repo_path)
        obj = object_read(repo, object_find(repo, commit))

        if obj.fmt == b"commit":
            obj = object_read(repo, obj.kvlm[b"tree"].decode())

        if not os.path.exists(path):
            os.mkdir(path)

        tree_checkout(repo, obj, os.path.realpath(path))
        return {"message": "Checkout completed"}
