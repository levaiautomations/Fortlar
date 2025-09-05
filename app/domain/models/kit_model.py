from sqlalchemy import (
Column, Integer, String, Text, Boolean, DateTime, Numeric
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

from app.infrastructure.configs.base_mixin import BaseMixin

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Kit(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'kits'


    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False, unique=True, index=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text)
    categoria = Column(String(100))
    valor_total = Column(Numeric(10, 2), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)


    imagens = relationship('ImagemKit', back_populates='kit', cascade='all,delete-orphan')
    produtos = relationship('KitProduto', back_populates='kit', cascade='all,delete-orphan')

