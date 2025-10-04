"""Router para operações de Pedidos"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime

from app.infrastructure.configs.database_config import Session
from app.infrastructure.configs.session_config import get_session
from app.infrastructure.container.dependency_container import container

pedido_router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"],
    responses={
        404: {"description": "Pedido não encontrado"},
        422: {"description": "Dados inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)


@pedido_router.get(
    "/",
    summary="Listar pedidos",
    description="Lista todos os pedidos com filtros opcionais"
)
async def list_pedidos(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    cliente_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    cupom_id: Optional[int] = Query(None, description="Filtrar por cupom"),
    start_date: Optional[datetime] = Query(None, description="Data inicial"),
    end_date: Optional[datetime] = Query(None, description="Data final"),
    min_value: Optional[float] = Query(None, ge=0, description="Valor mínimo"),
    max_value: Optional[float] = Query(None, ge=0, description="Valor máximo"),
    session: Session = Depends(get_session)
) -> List[dict]:
    """Lista pedidos com filtros opcionais"""
    try:
        pedido_repo = container.pedido_repository
        
        if cliente_id:
            pedidos = pedido_repo.get_by_cliente(cliente_id, session)
        elif status:
            from app.domain.models.pedido_model import PedidoStatusEnum
            status_enum = PedidoStatusEnum(status)
            pedidos = pedido_repo.get_by_status(status_enum, session)
        elif cupom_id:
            pedidos = pedido_repo.get_by_cupom(cupom_id, session)
        elif start_date and end_date:
            pedidos = pedido_repo.get_by_date_range(start_date, end_date, session)
        elif min_value is not None and max_value is not None:
            from decimal import Decimal
            pedidos = pedido_repo.get_orders_by_value_range(
                Decimal(str(min_value)), 
                Decimal(str(max_value)), 
                session
            )
        else:
            pedidos = pedido_repo.get_all(session, skip, limit)
        
        return [
            {
                "id": ped.id,
                "id_cliente": ped.id_cliente,
                "id_cupom": ped.cupom_id,
                "data_pedido": ped.data_pedido.isoformat(),
                "status": ped.status.value,
                "valor_total": float(ped.valor_total),
                "created_at": ped.created_at.isoformat(),
                "updated_at": ped.updated_at.isoformat()
            }
            for ped in pedidos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {str(e)}")


@pedido_router.get(
    "/{pedido_id}",
    summary="Buscar pedido por ID",
    description="Busca um pedido específico pelo ID"
)
async def get_pedido(
    pedido_id: int = Path(..., description="ID do pedido"),
    include_items: bool = Query(False, description="Incluir itens do pedido"),
    session: Session = Depends(get_session)
) -> dict:
    """Busca pedido por ID"""
    try:
        pedido_repo = container.pedido_repository
        
        if include_items:
            pedido = pedido_repo.get_orders_with_items(pedido_id, session)
        else:
            pedido = pedido_repo.get_by_id(pedido_id, session)
        
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        result = {
            "id": pedido.id,
            "id_cliente": pedido.id_cliente,
            "id_cupom": pedido.cupom_id,
            "data_pedido": pedido.data_pedido.isoformat(),
            "status": pedido.status.value,
            "valor_total": float(pedido.valor_total),
            "created_at": pedido.created_at.isoformat(),
            "updated_at": pedido.updated_at.isoformat()
        }
        
        if include_items and hasattr(pedido, 'itens'):
            result["itens"] = [
                {
                    "id": item.id,
                    "id_produto": item.id_produto,
                    "quantidade": item.quantidade,
                    "preco_unitario": float(item.preco_unitario),
                    "subtotal": float(item.subtotal)
                }
                for item in pedido.itens
            ]
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pedido: {str(e)}")


@pedido_router.get(
    "/cliente/{cliente_id}",
    summary="Listar pedidos do cliente",
    description="Lista todos os pedidos de um cliente específico"
)
async def list_pedidos_by_cliente(
    cliente_id: int = Path(..., description="ID do cliente"),
    session: Session = Depends(get_session)
) -> List[dict]:
    """Lista pedidos de um cliente"""
    try:
        pedido_repo = container.pedido_repository
        pedidos = pedido_repo.get_by_cliente(cliente_id, session)
        
        return [
            {
                "id": ped.id,
                "id_cliente": ped.id_cliente,
                "id_cupom": ped.cupom_id,
                "data_pedido": ped.data_pedido.isoformat(),
                "status": ped.status.value,
                "valor_total": float(ped.valor_total),
                "created_at": ped.created_at.isoformat(),
                "updated_at": ped.updated_at.isoformat()
            }
            for ped in pedidos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos do cliente: {str(e)}")


@pedido_router.get(
    "/status/{status}",
    summary="Listar pedidos por status",
    description="Lista pedidos com um status específico"
)
async def list_pedidos_by_status(
    status: str = Path(..., description="Status do pedido"),
    session: Session = Depends(get_session)
) -> List[dict]:
    """Lista pedidos por status"""
    try:
        from app.domain.models.pedido_model import PedidoStatusEnum
        pedido_repo = container.pedido_repository
        
        try:
            status_enum = PedidoStatusEnum(status)
        except ValueError:
            raise HTTPException(status_code=422, detail="Status inválido")
        
        pedidos = pedido_repo.get_by_status(status_enum, session)
        
        return [
            {
                "id": ped.id,
                "id_cliente": ped.id_cliente,
                "id_cupom": ped.cupom_id,
                "data_pedido": ped.data_pedido.isoformat(),
                "status": ped.status.value,
                "valor_total": float(ped.valor_total),
                "created_at": ped.created_at.isoformat(),
                "updated_at": ped.updated_at.isoformat()
            }
            for ped in pedidos
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos por status: {str(e)}")


@pedido_router.get(
    "/recentes",
    summary="Listar pedidos recentes",
    description="Lista pedidos dos últimos X dias"
)
async def list_pedidos_recentes(
    days: int = Query(7, ge=1, le=365, description="Número de dias"),
    session: Session = Depends(get_session)
) -> List[dict]:
    """Lista pedidos recentes"""
    try:
        pedido_repo = container.pedido_repository
        pedidos = pedido_repo.get_recent_orders(days, session)
        
        return [
            {
                "id": ped.id,
                "id_cliente": ped.id_cliente,
                "id_cupom": ped.cupom_id,
                "data_pedido": ped.data_pedido.isoformat(),
                "status": ped.status.value,
                "valor_total": float(ped.valor_total),
                "created_at": ped.created_at.isoformat(),
                "updated_at": ped.updated_at.isoformat()
            }
            for ped in pedidos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos recentes: {str(e)}")
