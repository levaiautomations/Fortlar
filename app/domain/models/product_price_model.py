from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from decimal import Decimal

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin

# Imports para relacionamentos (PrecoProduto é "filho", usa strings nas relationships)


class ProductPrice(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Preço do Product por Região e Prazo"""
    __tablename__ = 'precos_produto'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_produto: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('produtos.id_produto', ondelete='CASCADE'), 
        nullable=False
    )
    id_regiao: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('regioes.id', ondelete='RESTRICT'), 
        nullable=False
    )
    id_prazo: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('prazos_pagamento.id', ondelete='RESTRICT'), 
        nullable=False
    )
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    produto: Mapped[Optional['Product']] = relationship('Product')
    regiao: Mapped[Optional['Regions']] = relationship('Regions', back_populates='precos')
    prazo: Mapped[Optional['PaymentTerm']] = relationship('PaymentTerm', back_populates='precos')

    def __init__(self, id_produto, id_regiao, id_prazo, preco):
        self.id_produto = id_produto
        self.id_regiao = id_regiao
        self.id_prazo = id_prazo
        self.preco = preco

    # opcional: UniqueConstraint(produto_id, regiao_id, prazo_id)