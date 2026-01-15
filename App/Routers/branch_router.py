from fastapi import APIRouter
from Controllers.branch_controller import(
    get_branches as gt, 
    create_branch as cb
)

router = APIRouter(
    prefix="/repositories/{repo_path}/branches",
    tags=["Branches"]
)

@router.get("/")
def get_branches(repo_path: str):
    return gt(repo_path)

@router.post("/")
def create_branch(repo_path: str, name: str, commit: str):
    return cb(repo_path, name, commit)
