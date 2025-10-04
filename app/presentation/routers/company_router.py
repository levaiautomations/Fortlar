from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from typing import List, Optional

from app.application.usecases.impl.create_company_use_case import CreateCompanyUseCase
from app.application.usecases.impl.list_companies_use_case import ListCompaniesUseCase
from app.application.usecases.impl.get_company_use_case import GetCompanyUseCase
from app.application.usecases.impl.update_company_use_case import UpdateCompanyUseCase
from app.application.usecases.impl.delete_company_use_case import DeleteCompanyUseCase
from app.domain.exceptions.company_exceptions import CompanyAlreadyExistsException, CompanyNotFoundException
from app.infrastructure.configs.database_config import Session
from app.infrastructure.configs.session_config import get_session
from app.infrastructure.container.dependency_container import container
from app.presentation.routers.request.company_request import CompanyRequest
from app.presentation.routers.response.company_response import CompanyResponse

company_router = APIRouter(
    prefix="/companies",
    tags=["Empresas"],
    responses={
        404: {"description": "Empresa não encontrada"},
        422: {"description": "Dados inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)


# Dependencies
def get_create_company_use_case() -> CreateCompanyUseCase:
    return container.create_company_use_case

def get_list_companies_use_case() -> ListCompaniesUseCase:
    return container.list_companies_use_case

def get_get_company_use_case() -> GetCompanyUseCase:
    return container.get_company_use_case

def get_update_company_use_case() -> UpdateCompanyUseCase:
    return container.update_company_use_case

def get_delete_company_use_case() -> DeleteCompanyUseCase:
    return container.delete_company_use_case


@company_router.post(
    "/",
    response_model=CompanyResponse,
    status_code=201,
    summary="Criar empresa",
    description="Cria uma nova empresa no sistema com endereço e contato"
)
async def create_company(
    request: CompanyRequest,
    session: Session = Depends(get_session),
    use_case: CreateCompanyUseCase = Depends(get_create_company_use_case)
) -> CompanyResponse:
    """Cria uma nova empresa"""
    try:
        return use_case.execute(request, session=session)
    except CompanyAlreadyExistsException as e:
        raise HTTPException(status_code=422, detail=e.message)


@company_router.get(
    "/",
    response_model=List[CompanyResponse],
    summary="Listar empresas",
    description="Lista todas as empresas com filtros opcionais"
)
async def list_companies(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    active_only: bool = Query(False, description="Filtrar apenas empresas ativas"),
    vendedor_id: Optional[int] = Query(None, description="Filtrar por vendedor"),
    search_name: Optional[str] = Query(None, description="Buscar por nome"),
    session: Session = Depends(get_session),
    use_case: ListCompaniesUseCase = Depends(get_list_companies_use_case)
) -> List[CompanyResponse]:
    """Lista empresas com filtros opcionais"""
    request = {
        "skip": skip,
        "limit": limit,
        "active_only": active_only,
        "vendedor_id": vendedor_id,
        "search_name": search_name
    }
    return use_case.execute(request, session=session)


@company_router.get(
    "/{company_id}",
    response_model=CompanyResponse,
    summary="Buscar empresa por ID",
    description="Busca uma empresa específica pelo ID"
)
async def get_company(
    company_id: int = Path(..., description="ID da empresa"),
    session: Session = Depends(get_session),
    use_case: GetCompanyUseCase = Depends(get_get_company_use_case)
) -> CompanyResponse:
    """Busca empresa por ID"""
    try:
        return use_case.execute(company_id, session=session)
    except CompanyNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@company_router.put(
    "/{company_id}",
    response_model=CompanyResponse,
    summary="Atualizar empresa",
    description="Atualiza dados de uma empresa existente"
)
async def update_company(
    company_id: int = Path(..., description="ID da empresa"),
    razao_social: Optional[str] = Query(None, description="Razão social"),
    nome_fantasia: Optional[str] = Query(None, description="Nome fantasia"),
    ativo: Optional[bool] = Query(None, description="Status ativo/inativo"),
    session: Session = Depends(get_session),
    use_case: UpdateCompanyUseCase = Depends(get_update_company_use_case)
) -> CompanyResponse:
    """Atualiza empresa"""
    request = {
        "company_id": company_id,
        "razao_social": razao_social,
        "nome_fantasia": nome_fantasia,
        "ativo": ativo
    }
    try:
        return use_case.execute(request, session=session)
    except CompanyNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@company_router.delete(
    "/{company_id}",
    status_code=204,
    summary="Deletar empresa",
    description="Remove uma empresa do sistema"
)
async def delete_company(
    company_id: int = Path(..., description="ID da empresa"),
    session: Session = Depends(get_session),
    use_case: DeleteCompanyUseCase = Depends(get_delete_company_use_case)
):
    """Deleta empresa"""
    try:
        use_case.execute(company_id, session=session)
        return JSONResponse(content=None, status_code=204)
    except CompanyNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
