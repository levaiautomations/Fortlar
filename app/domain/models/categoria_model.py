from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin

# Imports para relacionamentos
from app.domain.models.subcategoria_model import Subcategoria
from app.domain.models.produto_model import Produto


class Categoria(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Categoria"""
    __tablename__ = 'categoria'

    id_categoria: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)

    # Relacionamentos
    subcategorias: Mapped[List['Subcategoria']] = relationship(
        'Subcategoria', 
        back_populates='categoria', 
        cascade='all,delete-orphan'
    )
    produtos: Mapped[List['Produto']] = relationship('Produto', back_populates='categoria')