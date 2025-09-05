from sqlalchemy import (
Column, Integer, String, Boolean, Date, DateTime, Numeric, CheckConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

from app.infrastructure.configs.base_mixin import BaseMixin

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Cupom(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'cupons'


    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False, unique=True, index=True)
    tipo = Column(String(20), nullable=False) # 'percentual' | 'valor_fixo'
    valor = Column(Numeric(10, 2), nullable=False)
    validade_inicio = Column(Date)
    validade_fim = Column(Date)
    ativo = Column(Boolean, nullable=False, default=True)


    __table_args__ = (
        CheckConstraint("tipo IN ('percentual','valor_fixo')", name='chk_cupons_tipo'),
    )


    pedidos = relationship('Pedido', back_populates='cupom')