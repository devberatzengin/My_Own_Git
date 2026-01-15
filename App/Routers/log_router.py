from fastapi import APIRouter
from Controllers.log_controller import *

router = APIRouter(
    prefix="/repositories/{repo_path}/log",
    tags=["Log"]
)

@router.get("/")
def get_log(repo_path: str, commit: str = "HEAD"):
    return get_log_controller(repo_path, commit)
