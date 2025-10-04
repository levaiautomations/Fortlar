"""Router para operações de Produtos"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from typing import List, Optional

from app.application.usecases.impl.list_produtos_use_case import ListProdutosUseCase
from app.infrastructure.configs.database_config import Session
from app.infrastructure.configs.session_config import get_session
from app.infrastructure.container.dependency_container import container

produto_router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"],
    responses={
        404: {"description": "Produto não encontrado"},
        422: {"description": "Dados inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)


# Dependencies
def get_list_produtos_use_case() -> ListProdutosUseCase:
    return container.list_produtos_use_case


@produto_router.get(
    "/",
    summary="Listar produtos",
    description="Lista todos os produtos com filtros opcionais"
)
async def list_produtos(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    active_only: bool = Query(True, description="Filtrar apenas produtos ativos"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoria"),
    subcategoria_id: Optional[int] = Query(None, description="Filtrar por subcategoria"),
    search_name: Optional[str] = Query(None, description="Buscar por nome"),
    min_price: Optional[float] = Query(None, ge=0, description="Preço mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Preço máximo"),
    session: Session = Depends(get_session),
    use_case: ListProdutosUseCase = Depends(get_list_produtos_use_case)
) -> List[dict]:
    """Lista produtos com filtros opcionais"""
    request = {
        "skip": skip,
        "limit": limit,
        "active_only": active_only,
        "categoria_id": categoria_id,
        "subcategoria_id": subcategoria_id,
        "search_name": search_name,
        "min_price": min_price,
        "max_price": max_price
    }
    return use_case.execute(request, session=session)


@produto_router.get(
    "/categoria/{categoria_id}",
    summary="Listar produtos por categoria",
    description="Lista produtos de uma categoria específica"
)
async def list_produtos_by_categoria(
    categoria_id: int = Path(..., description="ID da categoria"),
    active_only: bool = Query(True, description="Filtrar apenas produtos ativos"),
    session: Session = Depends(get_session),
    use_case: ListProdutosUseCase = Depends(get_list_produtos_use_case)
) -> List[dict]:
    """Lista produtos por categoria"""
    request = {
        "categoria_id": categoria_id,
        "active_only": active_only
    }
    return use_case.execute(request, session=session)


@produto_router.get(
    "/subcategoria/{subcategoria_id}",
    summary="Listar produtos por subcategoria",
    description="Lista produtos de uma subcategoria específica"
)
async def list_produtos_by_subcategoria(
    subcategoria_id: int = Path(..., description="ID da subcategoria"),
    active_only: bool = Query(True, description="Filtrar apenas produtos ativos"),
    session: Session = Depends(get_session),
    use_case: ListProdutosUseCase = Depends(get_list_produtos_use_case)
) -> List[dict]:
    """Lista produtos por subcategoria"""
    request = {
        "subcategoria_id": subcategoria_id,
        "active_only": active_only
    }
    return use_case.execute(request, session=session)


@produto_router.get(
    "/search",
    summary="Buscar produtos",
    description="Busca produtos por nome ou descrição"
)
async def search_produtos(
    q: str = Query(..., description="Termo de busca"),
    active_only: bool = Query(True, description="Filtrar apenas produtos ativos"),
    session: Session = Depends(get_session),
    use_case: ListProdutosUseCase = Depends(get_list_produtos_use_case)
) -> List[dict]:
    """Busca produtos por termo"""
    request = {
        "search_name": q,
        "active_only": active_only
    }
    return use_case.execute(request, session=session)


@produto_router.get(
    "/price-range",
    summary="Listar produtos por faixa de preço",
    description="Lista produtos dentro de uma faixa de preço"
)
async def list_produtos_by_price_range(
    min_price: float = Query(..., ge=0, description="Preço mínimo"),
    max_price: float = Query(..., ge=0, description="Preço máximo"),
    active_only: bool = Query(True, description="Filtrar apenas produtos ativos"),
    session: Session = Depends(get_session),
    use_case: ListProdutosUseCase = Depends(get_list_produtos_use_case)
) -> List[dict]:
    """Lista produtos por faixa de preço"""
    request = {
        "min_price": min_price,
        "max_price": max_price,
        "active_only": active_only
    }
    return use_case.execute(request, session=session)
