from sqlalchemy import (
Column, Integer, DateTime, Numeric, ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

from app.infrastructure.configs.base_mixin import BaseMixin

Base = declarative_base()



class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class PrecoProduto(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'precos_produto'


    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False)
    regiao_id = Column(Integer, ForeignKey('regioes.id', ondelete='RESTRICT'), nullable=False)
    prazo_id = Column(Integer, ForeignKey('prazos_pagamento.id', ondelete='RESTRICT'), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)


    produto = relationship('Produto')
    regiao = relationship('Regioes', back_populates='precos')
    prazo = relationship('PrazoPagamento', back_populates='precos')


    # opcional: UniqueConstraint(produto_id, regiao_id, prazo_id)