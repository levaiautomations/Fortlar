from sqlalchemy import Integer, String, Text, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from decimal import Decimal

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin

# Imports para relacionamentos
from app.domain.models.categoria_model import Categoria
from app.domain.models.subcategoria_model import Subcategoria


class Produto(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Produto"""
    __tablename__ = 'produtos'

    id_produto: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    id_categoria: Mapped[int] = mapped_column(Integer, ForeignKey('categoria.id_categoria'), nullable=False)
    id_subcategoria: Mapped[int] = mapped_column(Integer, ForeignKey('subcategoria.id_subcategoria'), nullable=False)
    valor_base: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relacionamentos
    categoria: Mapped[Optional['Categoria']] = relationship('Categoria', back_populates='produtos')
    subcategoria: Mapped[Optional['Subcategoria']] = relationship('Subcategoria', back_populates='produtos')
    # imagens: Mapped[List['ImagemProduto']] = relationship(
    #     'ImagemProduto', 
    #     back_populates='produto', 
    #     cascade='all,delete-orphan'
    # )
    # itens_pedido: Mapped[List['ItemPedido']] = relationship('ItemPedido', back_populates='produto')
    # kits_assoc: Mapped[List['KitProduto']] = relationship('KitProduto', back_populates='produto')