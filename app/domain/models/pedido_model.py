from sqlalchemy import (
Column, Integer, DateTime, Numeric, ForeignKey, Enum as SAEnum
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

from app.infrastructure.configs.base_mixin import BaseMixin

Base = declarative_base()


PEDIDO_STATUS = ('pendente', 'confirmado', 'em_preparacao', 'enviado', 'concluido', 'cancelado')


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class Pedido(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'pedidos'


    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('empresas.id'), nullable=False)
    cupom_id = Column(Integer, ForeignKey('cupons.id'), nullable=True)
    data_pedido = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(SAEnum(*PEDIDO_STATUS, name='pedido_status'), nullable=False, server_default='pendente')
    valor_total = Column(Numeric(10, 2), nullable=False)


    cliente = relationship('Empresa', back_populates='pedidos')
    cupom = relationship('Cupom', back_populates='pedidos')
    itens = relationship('ItemPedido', back_populates='pedido', cascade='all,delete-orphan')