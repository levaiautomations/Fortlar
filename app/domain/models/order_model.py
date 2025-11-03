from sqlalchemy import Integer, DateTime, Numeric, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from enum import Enum as PyEnum

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin

# Imports para relacionamentos
from app.domain.models.coupon_model import Coupon


class OrderStatusEnum(PyEnum):
    """Enum para status do pedido"""
    PENDENTE = 'pendente'
    CONFIRMADO = 'confirmado'
    EM_PREPARACAO = 'em_preparacao'
    ENVIADO = 'enviado'
    CONCLUIDO = 'concluido'
    CANCELADO = 'cancelado'


class Order(Base, TimestampMixin, BaseMixin):
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
    status: Mapped[OrderStatusEnum] = mapped_column(
        Enum(OrderStatusEnum, name='pedido_status'), 
        nullable=False, 
        default=OrderStatusEnum.PENDENTE
    )
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    cliente: Mapped[Optional['Company']] = relationship('Company')
    cupom: Mapped[Optional['Coupon']] = relationship('Coupon', back_populates='pedidos')
    # itens: Mapped[List['OrderItem']] = relationship(
    #     'OrderItem', 
    #     back_populates='pedido', 
    #     cascade='all,delete-orphan'
    # )

    def __init__(self, id_cliente, valor_total, cupom_id=None, status=OrderStatusEnum.PENDENTE):
        self.id_cliente = id_cliente
        self.cupom_id = cupom_id
        self.status = status
        self.valor_total = valor_total