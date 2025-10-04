from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from decimal import Decimal

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin


class PrazoPagamento(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Prazo de Pagamento"""
    __tablename__ = 'prazos_pagamento'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    percentual: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    precos: Mapped[List['PrecoProduto']] = relationship('PrecoProduto', back_populates='prazo')