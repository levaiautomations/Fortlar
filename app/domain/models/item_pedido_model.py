from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from decimal import Decimal

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin


class ItemPedido(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Item do Pedido"""
    __tablename__ = 'itens_pedido'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_pedido: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('pedidos.id_pedido', ondelete='CASCADE'), 
        nullable=False
    )
    id_produto: Mapped[int] = mapped_column(Integer, ForeignKey('produtos.id_produto'), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    pedido: Mapped[Optional['Pedido']] = relationship('Pedido', back_populates='itens')
    produto: Mapped[Optional['Produto']] = relationship('Produto', back_populates='itens_pedido')