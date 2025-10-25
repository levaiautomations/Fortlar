"""DTOs para requests de pedidos"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ListPedidosRequest(BaseModel):
    """Request para listar pedidos"""
    skip: int = Field(0, ge=0, description="Número de registros para pular")
    limit: int = Field(100, ge=1, le=1000, description="Número máximo de registros")
    cliente_id: Optional[int] = Field(None, description="Filtrar por cliente")
    status: Optional[str] = Field(None, description="Filtrar por status")
    cupom_id: Optional[int] = Field(None, description="Filtrar por cupom")
    start_date: Optional[datetime] = Field(None, description="Data inicial")
    end_date: Optional[datetime] = Field(None, description="Data final")
    min_value: Optional[float] = Field(None, ge=0, description="Valor mínimo")
    max_value: Optional[float] = Field(None, ge=0, description="Valor máximo")


class GetPedidoRequest(BaseModel):
    """Request para buscar pedido por ID"""
    pedido_id: int = Field(..., description="ID do pedido")
    include_items: bool = Field(False, description="Incluir itens do pedido")


class ListPedidosByClienteRequest(BaseModel):
    """Request para listar pedidos por cliente"""
    cliente_id: int = Field(..., description="ID do cliente")


class ListPedidosByStatusRequest(BaseModel):
    """Request para listar pedidos por status"""
    status: str = Field(..., description="Status do pedido")


class ListPedidosRecentesRequest(BaseModel):
    """Request para listar pedidos recentes"""
    days: int = Field(7, ge=1, le=365, description="Número de dias")
