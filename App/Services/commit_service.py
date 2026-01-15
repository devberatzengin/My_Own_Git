from datetime import datetime
from Core.libwyag import (
    repo_find,
    index_read,
    tree_from_index,
    commit_create,
    object_find,
    branch_get_active,
    gitconfig_read,
    gitconfig_user_get,
    repo_file,
    object_read
)


class CommitService:

    def create_commit(self, repo_path: str, message: str):
        repo = repo_find(repo_path)

        index = index_read(repo)
        tree_sha = tree_from_index(repo, index)
        parent_sha = object_find(repo, "HEAD")

        author = gitconfig_user_get(gitconfig_read())
        if not author:
            raise Exception("Git user.name ve user.email ayarlı değil")

        commit_sha = commit_create(
            repo=repo,
            tree=tree_sha,
            parent=parent_sha,
            author=author,
            timestamp=datetime.now(),
            message=message
        )

        self._update_head(repo, commit_sha)
        return {"commit_hash": commit_sha}

    def get_commits(self, repo_path: str):
        repo = repo_find(repo_path)
        head = object_find(repo, "HEAD")
        commits = []

        while head:
            commit = object_read(repo, head)
            commits.append({
                "hash": head,
                "message": commit.kvlm[None].decode().strip()
            })
            parent = commit.kvlm.get(b"parent")
            head = parent.decode() if parent else None

        return commits

    def get_commit_by_hash(self, repo_path: str, commit_hash: str):
        repo = repo_find(repo_path)
        commit = object_read(repo, commit_hash)

        return {
            "hash": commit_hash,
            "message": commit.kvlm[None].decode().strip(),
            "author": commit.kvlm[b"author"].decode()
        }

    def _update_head(self, repo, commit_sha: str):
        active_branch = branch_get_active(repo)

        if active_branch:
            with open(repo_file(repo, f"refs/heads/{active_branch}"), "w") as f:
                f.write(commit_sha + "\n")
        else:
            with open(repo_file(repo, "HEAD"), "w") as f:
                f.write(commit_sha + "\n")
