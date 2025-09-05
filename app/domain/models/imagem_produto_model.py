from sqlalchemy import (
Column, Integer, Text, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

from app.infrastructure.configs.base_mixin import BaseMixin

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class ImagemProduto(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'imagens_produto'


    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False)
    url = Column(Text, nullable=False)


    produto = relationship('Produto', back_populates='imagens')