from sqlalchemy import (
Column, Integer, String, DateTime

)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

from app.infrastructure.configs.base_mixin import BaseMixin

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class RamoAtividade(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'ramo_atividade'


    id = Column(Integer, primary_key=True)
    descricao = Column(String(150), nullable=False)


    empresas = relationship('Empresa', back_populates='ramo')