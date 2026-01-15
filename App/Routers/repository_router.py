from fastapi import APIRouter
from Controllers.repository_controller import *

router = APIRouter(prefix="/repositories", tags=["Repositories"])

@router.post("/")
def create_repo(repo_path: str):
    return create_repository(repo_path)

@router.get("/")
def get_all_repo():
    return get_repositories()

@router.get("/{repo_path}")
def get_repo(repo_path: str):
    return get_repo_by_path(repo_path)

@router.put("/{repo_path}")
def update_repo(repo_path: str):
    return update_repo_by_path(repo_path)

@router.delete("/{repo_path}")
def delete_repo(repo_path: str):
    return delete_repo_by_path(repo_path)

@router.get("/{repo_path}/branches")
def get_branches(repo_path: str):
    return get_repository_branches(repo_path)
