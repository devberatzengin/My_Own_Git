from Core.libwyag import repo_find, ref_create, ref_list

class BranchService:

    def get_branches(self, repo_path: str):
        repo = repo_find(repo_path)
        refs = ref_list(repo)
        return refs.get("heads", {})

    def create_branch(self, repo_path: str, name: str, commit: str):
        repo = repo_find(repo_path)
        ref_create(repo, f"heads/{name}", commit)
        return {"branch": name, "commit": commit}
