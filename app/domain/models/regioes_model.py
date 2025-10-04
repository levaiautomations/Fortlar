from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from decimal import Decimal

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin


class Regioes(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Regiões"""
    __tablename__ = 'regioes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estado: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    desconto_0: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    desconto_30: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    desconto_60: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    precos: Mapped[List['PrecoProduto']] = relationship('PrecoProduto', back_populates='regiao')