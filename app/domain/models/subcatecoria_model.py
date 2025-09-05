from sqlalchemy import (
Column, Integer, DateTime, ForeignKey, UniqueConstraint, String
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

from app.infrastructure.configs.base_mixin import BaseMixin

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)



class Subcategoria(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'subcategoria'


    id = Column(Integer, primary_key=True)
    categoria_id = Column(Integer, ForeignKey('categoria.id', ondelete='CASCADE'), nullable=False)
    nome = Column(String(150), nullable=False)


    categoria = relationship('Categoria', back_populates='subcategorias')
    produtos = relationship('Produto', back_populates='subcategoria')


    __table_args__ = (
        UniqueConstraint('categoria_id', 'nome', name='uq_subcategoria_categoria_nome'),
    )


