from sqlalchemy import (
Column, Integer, DateTime, Numeric, String
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

from app.infrastructure.configs.base_mixin import BaseMixin

Base = declarative_base()



class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class PrazoPagamento(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'prazos_pagamento'


    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    percentual = Column(Numeric(10, 2), nullable=False)


    precos = relationship('PrecoProduto', back_populates='prazo')