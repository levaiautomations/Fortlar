from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin



class Subcategoria(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Subcategoria"""
    __tablename__ = 'subcategoria'

    id_subcategoria: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_categoria: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('categoria.id_categoria', ondelete='CASCADE'), 
        nullable=False
    )
    nome: Mapped[str] = mapped_column(String(150), nullable=False)

    # Relacionamentos
    categoria: Mapped['Categoria'] = relationship('Categoria', back_populates='subcategorias')
    produtos: Mapped[List['Produto']] = relationship('Produto', back_populates='subcategoria')




