"""Interface do repository para Subcategoria"""

from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.models.subcategoria_model import Subcategoria
from app.infrastructure.configs.database_config import Session


class ISubcategoriaRepository(ABC):
    """Interface para operações de Subcategoria"""

    @abstractmethod
    def create(self, subcategoria: Subcategoria, session: Session) -> Subcategoria:
        pass

    @abstractmethod
    def get_by_id(self, subcategoria_id: int, session: Session) -> Optional[Subcategoria]:
        pass

    @abstractmethod
    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[Subcategoria]:
        pass

    @abstractmethod
    def update(self, subcategoria: Subcategoria, session: Session) -> Subcategoria:
        pass

    @abstractmethod
    def delete(self, subcategoria_id: int, session: Session) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str, session: Session) -> Optional[Subcategoria]:
        pass

    @abstractmethod
    def get_by_categoria(self, categoria_id: int, session: Session) -> List[Subcategoria]:
        pass

    @abstractmethod
    def search_by_name(self, name: str, session: Session) -> List[Subcategoria]:
        pass

    @abstractmethod
    def exists_by_name(self, name: str, session: Session) -> bool:
        pass
