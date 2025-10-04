from sqlalchemy import Integer, DateTime, Numeric, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from enum import Enum as PyEnum

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin


class PedidoStatusEnum(PyEnum):
    """Enum para status do pedido"""
    PENDENTE = 'pendente'
    CONFIRMADO = 'confirmado'
    EM_PREPARACAO = 'em_preparacao'
    ENVIADO = 'enviado'
    CONCLUIDO = 'concluido'
    CANCELADO = 'cancelado'


class Pedido(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Pedido"""
    __tablename__ = 'pedidos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(Integer, ForeignKey('empresas.id_empresa'), nullable=False)
    cupom_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('cupons.id'), nullable=True)
    data_pedido: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    status: Mapped[PedidoStatusEnum] = mapped_column(
        Enum(PedidoStatusEnum, name='pedido_status'), 
        nullable=False, 
        default=PedidoStatusEnum.PENDENTE
    )
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    cliente: Mapped[Optional['Company']] = relationship('Company', back_populates='pedidos')
    cupom: Mapped[Optional['Cupom']] = relationship('Cupom', back_populates='pedidos')
    itens: Mapped[List['ItemPedido']] = relationship(
        'ItemPedido', 
        back_populates='pedido', 
        cascade='all,delete-orphan'
    )