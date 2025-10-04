from sqlalchemy import Integer, String, Boolean, Date, Numeric, CheckConstraint, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from decimal import Decimal
from datetime import date

from app.infrastructure.configs.base_mixin import BaseMixin, Base, TimestampMixin


class TipoCupomEnum(str, SAEnum):
    """Enum para tipo de cupom"""
    PERCENTUAL = 'percentual'
    VALOR_FIXO = 'valor_fixo'


class Cupom(Base, TimestampMixin, BaseMixin):
    """Modelo de domínio para Cupom"""
    __tablename__ = 'cupons'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    tipo: Mapped[TipoCupomEnum] = mapped_column(
        SAEnum(TipoCupomEnum, name='tipo_cupom'), 
        nullable=False
    )
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    validade_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    validade_fim: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __table_args__ = (
        CheckConstraint("tipo IN ('percentual','valor_fixo')", name='chk_cupons_tipo'),
    )

    # Relacionamentos
    pedidos: Mapped[List['Pedido']] = relationship('Pedido', back_populates='cupom')