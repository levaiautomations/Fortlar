from sqlalchemy import (
Column, Integer, String, DateTime, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.domain.models.enumerations.email_token_type_enumerations import EmailTokenTypeEnum
from app.infrastructure.configs.base_mixin import BaseMixin, Base


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class EmailToken(Base, TimestampMixin, BaseMixin):
    __tablename__ = 'email_token'

    id_email = Column(Integer, primary_key=True)
    id_empresa = Column(Integer, ForeignKey('empresas.id_empresa', ondelete='CASCADE'), nullable=False)
    tipo = Column(Enum(EmailTokenTypeEnum, name="email_token_type_enum"), nullable=False)
    token = Column(String(100))
    expires_at = Column(DateTime(timezone=True), server_default=func.now() + func.cast("1 hour", DateTime),
                        nullable=False)
    empresa = relationship('Company', back_populates='email_token')

    def __init__(
            self,
            id_email,
            id_empresa,
            tipo,
            token
    ):
        self.id_email = id_email
        self.id_empresa = id_empresa
        self.tipo = tipo
        self.token = token