from pydantic import BaseModel

class CheckoutSchema(BaseModel):
    target: str  # branch name veya commit hash
