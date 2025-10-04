"""Interface do repository para Kit"""

from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.models.kit_model import Kit
from app.infrastructure.configs.database_config import Session


class IKitRepository(ABC):
    """Interface para operações de Kit"""

    @abstractmethod
    def create(self, kit: Kit, session: Session) -> Kit:
        pass

    @abstractmethod
    def get_by_id(self, kit_id: int, session: Session) -> Optional[Kit]:
        pass

    @abstractmethod
    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[Kit]:
        pass

    @abstractmethod
    def update(self, kit: Kit, session: Session) -> Kit:
        pass

    @abstractmethod
    def delete(self, kit_id: int, session: Session) -> bool:
        pass

    @abstractmethod
    def get_by_codigo(self, codigo: str, session: Session) -> Optional[Kit]:
        pass

    @abstractmethod
    def get_active_kits(self, session: Session) -> List[Kit]:
        pass

    @abstractmethod
    def search_by_name(self, name: str, session: Session) -> List[Kit]:
        pass

    @abstractmethod
    def get_by_categoria(self, categoria: str, session: Session) -> List[Kit]:
        pass

    @abstractmethod
    def get_kits_with_products(self, session: Session) -> List[Kit]:
        pass
