from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.application.usecases.impl.valid_token_use_case import ValidTokenUseCase
from app.infrastructure.configs.database_config import Session
from app.infrastructure.configs.session_config import get_session
from app.presentation.routers.request.validate_token_request import ValidateTokenRequest

company_router = APIRouter()

@company_router.put("/")
async def validate_token_router(
    request: ValidateTokenRequest,
    session: Session = Depends(get_session)
):

    use_case = ValidTokenUseCase()

    response = use_case.execute(request, session=session)
    return JSONResponse(content= response, status_code=200)
