from sqlalchemy import (
Column, Integer, String, DateTime, ForeignKey

)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

from app.infrastructure.configs.base_mixin import BaseMixin

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class Contato(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'contatos'


    id = Column(Integer, primary_key=True)
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)
    nome = Column(String(150), nullable=False)
    telefone = Column(String(20))
    celular = Column(String(20))
    email = Column(String(150), nullable=False)


    empresa = relationship('Empresa', back_populates='contatos')