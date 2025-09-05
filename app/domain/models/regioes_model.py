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


class Regioes(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'regioes'


    id = Column(Integer, primary_key=True)
    estado = Column(String(100), nullable=False, unique=True)
    icms = Column(Numeric(10, 2), nullable=False)


    precos = relationship('PrecoProduto', back_populates='regiao')