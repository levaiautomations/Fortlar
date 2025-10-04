from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from decimal import Decimal

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin


class PrecoProduto(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Preço do Produto por Região e Prazo"""
    __tablename__ = 'precos_produto'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_produto: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('produtos.id_produto', ondelete='CASCADE'), 
        nullable=False
    )
    id_regiao: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('regioes.id_regiao', ondelete='RESTRICT'), 
        nullable=False
    )
    id_prazo: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('prazos_pagamento.id_prazo', ondelete='RESTRICT'), 
        nullable=False
    )
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    produto: Mapped[Optional['Produto']] = relationship('Produto')
    regiao: Mapped[Optional['Regioes']] = relationship('Regioes', back_populates='precos')
    prazo: Mapped[Optional['PrazoPagamento']] = relationship('PrazoPagamento', back_populates='precos')

    # opcional: UniqueConstraint(produto_id, regiao_id, prazo_id)