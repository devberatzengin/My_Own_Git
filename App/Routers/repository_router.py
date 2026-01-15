
from fastapi import APIRouter
from Controllers.repository_controller import (
    create_repo as cr,
    get_repositories,
    get_repository_branches,
    get_repo_by_path,
    update_repo_by_path,
    delete_repo_by_path,
    get_repo_log,
    checkout_repository
)

router = APIRouter(prefix="/repositories", tags=["Repositories"])

@router.post("/")
def create_repo(repo_path: str):
    return cr(repo_path)

@router.get("/{repo_path}")
def get_repo(repo_path: str):
    return get_repo_by_path(repo_path)

@router.put("/{repo_path}")
def update_repo(repo_path:str):
    return update_repo_by_path(repo_path)

@router.get("/")
def get_all_repo():
    return get_repositories()

@router.get("/{repo_path}/branches")
def get_repo_branches(repo_path: str):
    return get_repository_branches(repo_path)

@router.delete("/{repo_path}")
def delete_repo(repo_path: str):
    return delete_repo_by_path(repo_path)


@router.get("/{repo_path}/log")
def get_log(repo_path: str):
    return get_repo_log(repo_path)

@router.post("/{repo_path}/checkout")
def checkout(repo_path: str, target: str):
    return checkout_repository(repo_path, target)
