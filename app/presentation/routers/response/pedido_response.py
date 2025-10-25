"""DTOs para responses de pedidos"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class ItemPedidoResponse(BaseModel):
    """Response para item do pedido"""
    id: int
    id_produto: int
    quantidade: int
    preco_unitario: float
    subtotal: float


class PedidoResponse(BaseModel):
    """Response para pedido"""
    id: int
    id_cliente: int
    id_cupom: Optional[int]
    data_pedido: datetime
    status: str
    valor_total: float
    created_at: datetime
    updated_at: datetime
    itens: Optional[List[ItemPedidoResponse]] = None


class ListPedidosResponse(BaseModel):
    """Response para lista de pedidos"""
    pedidos: List[PedidoResponse]
    total: int
    skip: int
    limit: int
