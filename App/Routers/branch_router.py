from fastapi import APIRouter
from controllers.branch_controller import (
    create_branch,
    get_branches,
    get_branch_by_name,
    delete_branch_by_name
)

router = APIRouter(
    prefix="/repositories/{repo_path}/branches",
    tags=["Branches"]
)

@router.post("/")
def create_branch_route(repo_path: str, branch_name: str):
    return create_branch(repo_path, branch_name)

@router.get("/")
def get_all_branches(repo_path: str):
    return get_branches(repo_path)

@router.get("/{branch_name}")
def get_branch(repo_path: str, branch_name: str):
    return get_branch_by_name(repo_path, branch_name)

@router.delete("/{branch_name}")
def delete_branch(repo_path: str, branch_name: str):
    return delete_branch_by_name(repo_path, branch_name)
