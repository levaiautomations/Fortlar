"""DTOs para requests de pedidos"""

from typing import Optional, List
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


class ItemCarrinhoRequest(BaseModel):
    """Item do carrinho"""
    id_produto: int = Field(..., description="ID do produto")
    quantidade: int = Field(..., ge=1, description="Quantidade do produto")
    preco_unitario: float = Field(..., ge=0, description="Preço unitário do produto")


class EnvioPedidoRequest(BaseModel):
    """Request para envio de pedido"""
    id_cliente: int = Field(..., description="ID do cliente (empresa)")
    itens: List[ItemCarrinhoRequest] = Field(..., min_items=1, description="Lista de itens do carrinho")
    forma_pagamento: str = Field(..., description="Forma de pagamento")
