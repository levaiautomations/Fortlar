from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin


class KitProduto(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para associação Kit-Produto"""
    __tablename__ = 'kits_produtos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_kit: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('kits.id_kit', ondelete='CASCADE'), 
        nullable=False
    )
    id_produto: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('produtos.id_produto', ondelete='CASCADE'), 
        nullable=False
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Relacionamentos
    kit: Mapped[Optional['Kit']] = relationship('Kit', back_populates='produtos')
    produto: Mapped[Optional['Produto']] = relationship('Produto', back_populates='kits_assoc')

    __table_args__ = (
        UniqueConstraint('kit_id', 'produto_id', name='uq_kit_produto'),
    )