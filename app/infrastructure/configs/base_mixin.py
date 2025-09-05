from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BaseMixin:
    def to_dict(self):
        """Converte todos os campos da tabela em dicionário."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        """Retorna representação legível para debug."""
        attrs = ", ".join(f"{c.name}={getattr(self, c.name)!r}" for c in self.__table__.columns)
        return f"<{self.__class__.__name__}({attrs})>"

    def get(self, field):
        """Retorna o valor de um campo específico."""
        return getattr(self, field, None)

