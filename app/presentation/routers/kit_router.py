"""Router para operações de Kits"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from typing import List, Optional

from app.infrastructure.configs.database_config import Session
from app.infrastructure.configs.session_config import get_session
from app.infrastructure.container.dependency_container import container

kit_router = APIRouter(
    prefix="/kits",
    tags=["Kits"],
    responses={
        404: {"description": "Kit não encontrado"},
        422: {"description": "Dados inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)


@kit_router.get(
    "/",
    summary="Listar kits",
    description="Lista todos os kits com filtros opcionais"
)
async def list_kits(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    active_only: bool = Query(True, description="Filtrar apenas kits ativos"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    search_name: Optional[str] = Query(None, description="Buscar por nome"),
    min_price: Optional[float] = Query(None, ge=0, description="Preço mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Preço máximo"),
    with_products: bool = Query(False, description="Incluir apenas kits com produtos"),
    with_images: bool = Query(False, description="Incluir apenas kits com imagens"),
    session: Session = Depends(get_session)
) -> List[dict]:
    """Lista kits com filtros opcionais"""
    try:
        kit_repo = container.kit_repository
        
        if search_name:
            kits = kit_repo.search_by_name(search_name, session)
        elif categoria:
            kits = kit_repo.get_by_categoria(categoria, session)
        elif min_price is not None and max_price is not None:
            from decimal import Decimal
            kits = kit_repo.get_by_price_range(
                Decimal(str(min_price)), 
                Decimal(str(max_price)), 
                session
            )
        elif with_products:
            kits = kit_repo.get_kits_with_products(session)
        elif with_images:
            kits = kit_repo.get_kits_with_images(session)
        elif active_only:
            kits = kit_repo.get_active_kits(session)
        else:
            kits = kit_repo.get_all(session, skip, limit)
        
        return [
            {
                "id": kit.id,
                "codigo": kit.codigo,
                "nome": kit.nome,
                "descricao": kit.descricao,
                "categoria": kit.categoria,
                "valor_total": float(kit.valor_total),
                "ativo": kit.ativo,
                "created_at": kit.created_at.isoformat(),
                "updated_at": kit.updated_at.isoformat()
            }
            for kit in kits
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar kits: {str(e)}")


@kit_router.get(
    "/{kit_id}",
    summary="Buscar kit por ID",
    description="Busca um kit específico pelo ID"
)
async def get_kit(
    kit_id: int = Path(..., description="ID do kit"),
    include_products: bool = Query(False, description="Incluir produtos do kit"),
    include_images: bool = Query(False, description="Incluir imagens do kit"),
    session: Session = Depends(get_session)
) -> dict:
    """Busca kit por ID"""
    try:
        kit_repo = container.kit_repository
        kit = kit_repo.get_by_id(kit_id, session)
        
        if not kit:
            raise HTTPException(status_code=404, detail="Kit não encontrado")
        
        result = {
            "id": kit.id,
            "codigo": kit.codigo,
            "nome": kit.nome,
            "descricao": kit.descricao,
            "categoria": kit.categoria,
            "valor_total": float(kit.valor_total),
            "ativo": kit.ativo,
            "created_at": kit.created_at.isoformat(),
            "updated_at": kit.updated_at.isoformat()
        }
        
        if include_products and hasattr(kit, 'produtos'):
            result["produtos"] = [
                {
                    "id": prod.id,
                    "codigo": prod.codigo,
                    "nome": prod.nome,
                    "quantidade": prod.quantidade if hasattr(prod, 'quantidade') else 1
                }
                for prod in kit.produtos
            ]
        
        if include_images and hasattr(kit, 'imagens'):
            result["imagens"] = [
                {
                    "id": img.id,
                    "url": img.url
                }
                for img in kit.imagens
            ]
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar kit: {str(e)}")


@kit_router.get(
    "/codigo/{codigo}",
    summary="Buscar kit por código",
    description="Busca um kit específico pelo código"
)
async def get_kit_by_codigo(
    codigo: str = Path(..., description="Código do kit"),
    session: Session = Depends(get_session)
) -> dict:
    """Busca kit por código"""
    try:
        kit_repo = container.kit_repository
        kit = kit_repo.get_by_codigo(codigo, session)
        
        if not kit:
            raise HTTPException(status_code=404, detail="Kit não encontrado")
        
        return {
            "id": kit.id,
            "codigo": kit.codigo,
            "nome": kit.nome,
            "descricao": kit.descricao,
            "categoria": kit.categoria,
            "valor_total": float(kit.valor_total),
            "ativo": kit.ativo,
            "created_at": kit.created_at.isoformat(),
            "updated_at": kit.updated_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar kit por código: {str(e)}")


@kit_router.get(
    "/categoria/{categoria}",
    summary="Listar kits por categoria",
    description="Lista kits de uma categoria específica"
)
async def list_kits_by_categoria(
    categoria: str = Path(..., description="Categoria do kit"),
    active_only: bool = Query(True, description="Filtrar apenas kits ativos"),
    session: Session = Depends(get_session)
) -> List[dict]:
    """Lista kits por categoria"""
    try:
        kit_repo = container.kit_repository
        kits = kit_repo.get_by_categoria(categoria, session)
        
        if active_only:
            kits = [k for k in kits if k.ativo]
        
        return [
            {
                "id": kit.id,
                "codigo": kit.codigo,
                "nome": kit.nome,
                "descricao": kit.descricao,
                "categoria": kit.categoria,
                "valor_total": float(kit.valor_total),
                "ativo": kit.ativo,
                "created_at": kit.created_at.isoformat(),
                "updated_at": kit.updated_at.isoformat()
            }
            for kit in kits
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar kits por categoria: {str(e)}")


@kit_router.get(
    "/search",
    summary="Buscar kits",
    description="Busca kits por nome ou descrição"
)
async def search_kits(
    q: str = Query(..., description="Termo de busca"),
    active_only: bool = Query(True, description="Filtrar apenas kits ativos"),
    session: Session = Depends(get_session)
) -> List[dict]:
    """Busca kits por termo"""
    try:
        kit_repo = container.kit_repository
        kits = kit_repo.search_by_name(q, session)
        
        if active_only:
            kits = [k for k in kits if k.ativo]
        
        return [
            {
                "id": kit.id,
                "codigo": kit.codigo,
                "nome": kit.nome,
                "descricao": kit.descricao,
                "categoria": kit.categoria,
                "valor_total": float(kit.valor_total),
                "ativo": kit.ativo,
                "created_at": kit.created_at.isoformat(),
                "updated_at": kit.updated_at.isoformat()
            }
            for kit in kits
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar kits: {str(e)}")
