from sqlalchemy import Integer, String, Text, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from decimal import Decimal

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin


class Kit(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Kit"""
    __tablename__ = 'kits'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    categoria: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relacionamentos comentados temporariamente
    # imagens: Mapped[List['ImagemKit']] = relationship(
    #     'ImagemKit', 
    #     back_populates='kit', 
    #     cascade='all,delete-orphan'
    # )
    # produtos: Mapped[List['KitProduto']] = relationship(
    #     'KitProduto', 
    #     back_populates='kit', 
    #     cascade='all,delete-orphan'
    # )

