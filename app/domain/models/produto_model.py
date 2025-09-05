from sqlalchemy import (
Column, Integer, String, Text, Boolean, DateTime, Numeric, ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Produto(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'produtos'


    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False, unique=True, index=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text)
    categoria_id = Column(Integer, ForeignKey('categoria.id'), nullable=False)
    subcategoria_id = Column(Integer, ForeignKey('subcategoria.id'), nullable=False)
    valor_base = Column(Numeric(10, 2), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)


    categoria = relationship('Categoria', back_populates='produtos')
    subcategoria = relationship('Subcategoria', back_populates='produtos')
    imagens = relationship('ImagemProduto', back_populates='produto', cascade='all,delete-orphan')
    itens_pedido = relationship('ItemPedido', back_populates='produto')
    kits_assoc = relationship('KitProduto', back_populates='produto')