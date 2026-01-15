from fastapi import APIRouter
from Controllers.checkout_controller import *

router = APIRouter(
    prefix="/repositories/{repo_path}/checkout",
    tags=["Checkout"]
)

@router.post("/")
def checkout(repo_path: str, commit: str, path: str):
    return checkout_controller(repo_path, commit, path)
