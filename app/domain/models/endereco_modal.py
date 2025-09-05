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



class Endereco(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'enderecos'


    id = Column(Integer, primary_key=True)
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)
    cep = Column(String(20), nullable=False)
    numero = Column(String(20), nullable=False)
    complemento = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(100))
    uf = Column(String(2), nullable=False)
    ibge = Column(String(20), nullable=False)


    empresa = relationship('Empresa', back_populates='enderecos')