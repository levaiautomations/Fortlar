from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.application.usecases.impl.login_use_case import LoginUseCase
from app.infrastructure.configs.database_config import Session
from app.infrastructure.configs.session_config import get_session
from app.presentation.routers.request.login_request import LoginRequest
from app.presentation.routers.response.login_response import LoginResponse

login_router = APIRouter()

@login_router.post("/login")
def login(
    request: LoginRequest,
    session: Session = Depends(get_session)
):
    """
    Endpoint para login de empresa.
    Retorna JWT se as credenciais estiverem corretas.
    """
    use_case = LoginUseCase()

    login_response: LoginResponse = use_case.execute(request, session).to_dict()
    return JSONResponse(content=login_response, status_code=200)
