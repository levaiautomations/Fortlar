from sqlalchemy import (
Column, Integer, String, DateTime, ForeignKey,

)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

from app.infrastructure.configs.base_mixin import BaseMixin

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class Empresa(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'empresas'


    id = Column(Integer, primary_key=True)
    cnpj = Column(String(20), nullable=False, unique=True, index=True)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255), nullable=False)
    senha_hash = Column(String(255), nullable=False)


    origem_id = Column(Integer, ForeignKey('origem.id'), nullable=False)
    regime_id = Column(Integer, ForeignKey('regime_tributario.id'), nullable=False)
    regiao_id = Column(Integer, ForeignKey('regiao.id'), nullable=False)
    ramo_id = Column(Integer, ForeignKey('ramo_atividade.id'), nullable=False)
    vendedor_id = Column(Integer, ForeignKey('vendedor.id'), nullable=False)


    data_cadastro = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


    # relações
    origem = relationship('Origem', back_populates='empresas')
    regime = relationship('RegimeTributario', back_populates='empresas')
    regiao = relationship('Regiao', back_populates='empresas')
    ramo = relationship('RamoAtividade', back_populates='empresas')
    vendedor = relationship('Vendedor', back_populates='empresas')


    enderecos = relationship('Endereco', back_populates='empresa', cascade='all,delete-orphan')
    contatos = relationship('Contato', back_populates='empresa', cascade='all,delete-orphan')
    pedidos = relationship('Pedido', back_populates='cliente', cascade='all,delete-orphan')

