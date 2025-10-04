from pydantic import BaseModel, EmailStr
from typing import Union

class LoginRequest(BaseModel):
    login: Union[EmailStr, str]  # Pode ser email ou CNPJ
    password: str
