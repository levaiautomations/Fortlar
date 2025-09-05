from sqlalchemy import (
Column, Integer, String, Text, Boolean, Date, DateTime, Numeric,
ForeignKey, CheckConstraint, UniqueConstraint, Index, Enum as SAEnum
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

from app.infrastructure.configs.base_mixin import BaseMixin

Base = declarative_base()


# Enum para status de pedido (mapeado para um ENUM nativo do Postgres quando possível)
PEDIDO_STATUS = ('pendente', 'confirmado', 'em_preparacao', 'enviado', 'concluido', 'cancelado')




class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class KitProduto(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'kits_produtos'


    id = Column(Integer, primary_key=True)
    kit_id = Column(Integer, ForeignKey('kits.id', ondelete='CASCADE'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)


    kit = relationship('Kit', back_populates='produtos')
    produto = relationship('Produto', back_populates='kits_assoc')


    __table_args__ = (
        UniqueConstraint('kit_id', 'produto_id', name='uq_kit_produto'),
    )