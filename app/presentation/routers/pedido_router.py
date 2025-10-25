"""Router para operações de Pedidos - Refatorado com Clean Architecture e SOLID"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from typing import List

# Use Cases
from app.application.usecases.impl.list_pedidos_use_case import ListPedidosUseCase
from app.application.usecases.impl.get_pedido_use_case import GetPedidoUseCase
from app.application.usecases.impl.list_pedidos_recentes_use_case import ListPedidosRecentesUseCase

# Repositories
from app.infrastructure.repositories.impl.pedido_repository_impl import PedidoRepository

# Configs
from app.infrastructure.configs.database_config import Session
from app.infrastructure.configs.session_config import get_session
from app.infrastructure.configs.security_config import verify_user_permission
from app.presentation.routers.request.pedido_request import (
    ListPedidosRequest,
    GetPedidoRequest,
    ListPedidosByClienteRequest,
    ListPedidosByStatusRequest,
    ListPedidosRecentesRequest
)
from app.presentation.routers.response.pedido_response import (
    PedidoResponse,
    ListPedidosResponse
)

pedido_router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"],
    responses={
        404: {"description": "Pedido não encontrado"},
        422: {"description": "Dados inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)


# Dependency Injection Functions removidas - usando padrão simples


@pedido_router.get(
    "/",
    summary="Listar pedidos",
    description="Lista todos os pedidos com filtros opcionais",
    response_model=List[PedidoResponse]
)
async def list_pedidos(
    request: ListPedidosRequest = Depends(),
    session: Session = Depends(get_session),
    current_user = Depends(verify_user_permission())
) -> List[PedidoResponse]:
    """
    Lista pedidos com filtros opcionais.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Open/Closed: Extensível via novos filtros sem modificar código existente
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: ListPedidosUseCase = ListPedidosUseCase()
        pedidos_data = use_case.execute(request.dict(), session)
        return [PedidoResponse(**pedido) for pedido in pedidos_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {str(e)}")


@pedido_router.get(
    "/{pedido_id}",
    summary="Buscar pedido por ID",
    description="Busca um pedido específico pelo ID",
    response_model=PedidoResponse
)
async def get_pedido(
    pedido_id: int = Path(..., description="ID do pedido"),
    include_items: bool = Query(False, description="Incluir itens do pedido"),
    session: Session = Depends(get_session),
    current_user = Depends(verify_user_permission())
) -> PedidoResponse:
    """
    Busca pedido por ID.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: GetPedidoUseCase = GetPedidoUseCase()
        request = GetPedidoRequest(pedido_id=pedido_id, include_items=include_items)
        pedido_data = use_case.execute(request.dict(), session)
        return PedidoResponse(**pedido_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pedido: {str(e)}")


@pedido_router.get(
    "/cliente/{cliente_id}",
    summary="Listar pedidos do cliente",
    description="Lista todos os pedidos de um cliente específico",
    response_model=List[PedidoResponse]
)
async def list_pedidos_by_cliente(
    cliente_id: int = Path(..., description="ID do cliente"),
    session: Session = Depends(get_session)
) -> List[PedidoResponse]:
    """
    Lista pedidos de um cliente específico.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: ListPedidosUseCase = ListPedidosUseCase()
        request = ListPedidosByClienteRequest(cliente_id=cliente_id)
        pedidos_data = use_case.execute(request.dict(), session)
        return [PedidoResponse(**pedido) for pedido in pedidos_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos do cliente: {str(e)}")


@pedido_router.get(
    "/status/{status}",
    summary="Listar pedidos por status",
    description="Lista pedidos com um status específico",
    response_model=List[PedidoResponse]
)
async def list_pedidos_by_status(
    status: str = Path(..., description="Status do pedido"),
    session: Session = Depends(get_session)
) -> List[PedidoResponse]:
    """
    Lista pedidos por status.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: ListPedidosUseCase = ListPedidosUseCase()
        request = ListPedidosByStatusRequest(status=status)
        pedidos_data = use_case.execute(request.dict(), session)
        return [PedidoResponse(**pedido) for pedido in pedidos_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos por status: {str(e)}")


@pedido_router.get(
    "/recentes",
    summary="Listar pedidos recentes",
    description="Lista pedidos dos últimos X dias",
    response_model=List[PedidoResponse]
)
async def list_pedidos_recentes(
    days: int = Query(7, ge=1, le=365, description="Número de dias"),
    session: Session = Depends(get_session)
) -> List[PedidoResponse]:
    """
    Lista pedidos recentes.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: ListPedidosRecentesUseCase = ListPedidosRecentesUseCase()
        request = ListPedidosRecentesRequest(days=days)
        pedidos_data = use_case.execute(request.dict(), session)
        return [PedidoResponse(**pedido) for pedido in pedidos_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos recentes: {str(e)}")
