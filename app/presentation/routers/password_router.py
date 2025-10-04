from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.application.usecases.impl.forgot_use_case import ForgotPasswordUseCase
from app.application.usecases.impl.reset_use_case import ResetPasswordUseCase
from app.infrastructure.configs.session_config import get_session
from app.infrastructure.configs.database_config import Session
from app.presentation.routers.request.forgot_password_request import ForgotPasswordRequest
from app.presentation.routers.request.reset_password_request import ResetPasswordRequest


password_router = APIRouter()

@password_router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, session: Session = Depends(get_session)):
    use_case = ForgotPasswordUseCase()
    use_case.execute(request, session)
    return JSONResponse(content={"message": "Se um e-mail válido foi encontrado, enviamos instruções de recuperação."}, status_code=200)


@password_router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, session: Session = Depends(get_session)):
    use_case = ResetPasswordUseCase()
    use_case.execute(request, session)
    return JSONResponse(content={"message": "Senha alterada com sucesso!"}, status_code=200)
