from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin


class ImagemProduto(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Imagem do Produto"""
    __tablename__ = 'imagens_produto'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_produto: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('produtos.id_produto', ondelete='CASCADE'), 
        nullable=False
    )
    url: Mapped[str] = mapped_column(Text, nullable=False)

    # Relacionamento
    produto: Mapped[Optional['Produto']] = relationship('Produto', back_populates='imagens')