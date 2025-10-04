from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin

# Imports para relacionamentos
from app.domain.models.company_model import Company


class Seller(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Vendedor"""
    __tablename__ = 'vendedor'

    id_vendedor: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)

    # Relacionamentos
    empresa: Mapped[List['Company']] = relationship('Company', back_populates='vendedor')
