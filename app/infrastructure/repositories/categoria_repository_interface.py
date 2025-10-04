"""Interface do repository para Categoria"""

from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.models.categoria_model import Categoria
from app.infrastructure.configs.database_config import Session


class ICategoriaRepository(ABC):
    """Interface para operações de Categoria"""

    @abstractmethod
    def create(self, categoria: Categoria, session: Session) -> Categoria:
        pass

    @abstractmethod
    def get_by_id(self, categoria_id: int, session: Session) -> Optional[Categoria]:
        pass

    @abstractmethod
    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[Categoria]:
        pass

    @abstractmethod
    def update(self, categoria: Categoria, session: Session) -> Categoria:
        pass

    @abstractmethod
    def delete(self, categoria_id: int, session: Session) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str, session: Session) -> Optional[Categoria]:
        pass

    @abstractmethod
    def search_by_name(self, name: str, session: Session) -> List[Categoria]:
        pass

    @abstractmethod
    def exists_by_name(self, name: str, session: Session) -> bool:
        pass
