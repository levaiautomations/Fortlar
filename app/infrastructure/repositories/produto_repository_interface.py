"""Interface do repository para Produto"""

from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.models.produto_model import Produto
from app.infrastructure.configs.database_config import Session


class IProdutoRepository(ABC):
    """Interface para operações de Produto"""

    @abstractmethod
    def create(self, produto: Produto, session: Session) -> Produto:
        pass

    @abstractmethod
    def get_by_id(self, produto_id: int, session: Session) -> Optional[Produto]:
        pass

    @abstractmethod
    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[Produto]:
        pass

    @abstractmethod
    def update(self, produto: Produto, session: Session) -> Produto:
        pass

    @abstractmethod
    def delete(self, produto_id: int, session: Session) -> bool:
        pass

    @abstractmethod
    def get_by_codigo(self, codigo: str, session: Session) -> Optional[Produto]:
        pass

    @abstractmethod
    def get_by_categoria(self, categoria_id: int, session: Session) -> List[Produto]:
        pass

    @abstractmethod
    def get_by_subcategoria(self, subcategoria_id: int, session: Session) -> List[Produto]:
        pass

    @abstractmethod
    def get_active_products(self, session: Session) -> List[Produto]:
        pass

    @abstractmethod
    def search_by_name(self, name: str, session: Session) -> List[Produto]:
        pass

    @abstractmethod
    def get_by_price_range(self, min_price: float, max_price: float, session: Session) -> List[Produto]:
        pass
