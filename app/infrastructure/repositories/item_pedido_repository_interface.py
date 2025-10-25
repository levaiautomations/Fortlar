from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.models.item_pedido_model import ItemPedido
from app.infrastructure.configs.database_config import Session


class IItemPedidoRepository(ABC):
    """Interface para operações de ItemPedido"""

    @abstractmethod
    def create(self, item_pedido: ItemPedido, session: Session) -> ItemPedido:
        """Cria um novo item de pedido"""
        pass

    @abstractmethod
    def get_by_id(self, item_id: int, session: Session) -> Optional[ItemPedido]:
        """Busca item de pedido por ID"""
        pass

    @abstractmethod
    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[ItemPedido]:
        """Lista todos os itens de pedido"""
        pass

    @abstractmethod
    def update(self, item_pedido: ItemPedido, session: Session) -> ItemPedido:
        """Atualiza um item de pedido"""
        pass

    @abstractmethod
    def delete(self, item_id: int, session: Session) -> bool:
        """Deleta um item de pedido"""
        pass

    @abstractmethod
    def get_by_pedido_id(self, pedido_id: int, session: Session) -> List[ItemPedido]:
        """Busca itens por ID do pedido"""
        pass

    @abstractmethod
    def get_by_produto_id(self, produto_id: int, session: Session) -> List[ItemPedido]:
        """Busca itens por ID do produto"""
        pass

    @abstractmethod
    def get_total_by_pedido(self, pedido_id: int, session: Session) -> float:
        """Calcula total dos itens de um pedido"""
        pass

    @abstractmethod
    def get_quantity_by_produto(self, produto_id: int, session: Session) -> int:
        """Calcula quantidade total vendida de um produto"""
        pass
