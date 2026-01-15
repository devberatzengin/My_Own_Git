from Services.branch_service import BranchService

branch_service = BranchService()

def get_branches(repo_path: str):
    return BranchService.get_branches(repo_path=repo_path)

def create_branch(repo_path:str, name:str , commit:str):
    return BranchService.create_branch(repo_path=repo_path, name=name, commit=commit)