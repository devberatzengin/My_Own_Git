
from Services.repository_service import RepositoryService

repository_service = RepositoryService()

def get_repositories():
    return repository_service.get_repositories()

def get_repository_branches(repository_path : str):
    return repository_service.get_repository_branches(repo_path=repository_path)

def get_repo_by_path(path:str):
    return repository_service.get_repo_by_path(repo_path=path)

def create_repository(path: str):
    return repository_service.create_repository(path)

def update_repo_by_path(path:str):
    return repository_service.update_repo_by_path(repo_path=path)

def delete_repo_by_path(path:str):
    return repository_service.delete_repo_by_path(repo_path=path)
