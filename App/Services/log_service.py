from Core.libwyag import repo_find, object_find, object_read

class LogService:

    def get_log(self, repo_path: str, commit: str = "HEAD"):
        repo = repo_find(repo_path)
        sha = object_find(repo, commit)
        logs = []

        while sha:
            obj = object_read(repo, sha)
            logs.append({
                "hash": sha,
                "message": obj.kvlm[None].decode().strip()
            })
            parent = obj.kvlm.get(b"parent")
            sha = parent.decode() if parent else None

        return logs
