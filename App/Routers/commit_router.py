from fastapi import APIRouter
from controllers.commit_controller import (
    create_commit,
    get_commits,
    get_commit_by_hash
)

router = APIRouter(
    prefix="/repositories/{repo_path}/commits",
    tags=["Commits"]
)

@router.post("/")
def create_commit_route(repo_path: str, message: str):
    return create_commit(repo_path, message)

@router.get("/")
def get_all_commits(repo_path: str):
    return get_commits(repo_path)

@router.get("/{commit_hash}")
def get_commit(repo_path: str, commit_hash: str):
    return get_commit_by_hash(repo_path, commit_hash)
