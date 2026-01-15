from Services.checkout_service import CheckoutService

checkout_service = CheckoutService()

def checkout(repo_path: str, commit : str, path :str):
    return CheckoutService.checkout( repo_path=repo_path, commit=commit, path=path)
