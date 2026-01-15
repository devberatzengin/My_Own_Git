from Core.libwyag import repo_create, repo_find, ref_list

class RepositoryService:

    def create_repository(self, path: str):
        repo_create(path)
        return {"message": "Repository created", "path": path}

    def get_repositories(self):
        # local filesystem based olduğu için basit tutuluyor
        return {"message": "Local repository mode (single repo supported)"}

    def get_repository_branches(self, repo_path: str):
        repo = repo_find(repo_path)
        refs = ref_list(repo)
        return refs.get("heads", {})

    def get_repo_by_path(self, repo_path: str):
        repo = repo_find(repo_path)
        return {
            "worktree": repo.worktree,
            "gitdir": repo.gitdir
        }

    def update_repo_by_path(self, repo_path: str):
        return {"message": "Nothing to update for filesystem repo"}

    def delete_repo_by_path(self, repo_path: str):
        return {"message": "Delete not supported (filesystem safety)"}
