from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin


class ImagemKit(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Imagem do Kit"""
    __tablename__ = 'imagens_kits'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_kit: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('kits.id_kit', ondelete='CASCADE'), 
        nullable=False
    )
    url: Mapped[str] = mapped_column(Text, nullable=False)

    # Relacionamento
    kit: Mapped[Optional['Kit']] = relationship('Kit', back_populates='imagens')