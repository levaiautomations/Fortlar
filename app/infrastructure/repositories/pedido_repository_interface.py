"""Interface do repository para Pedido"""

from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime

from app.domain.models.pedido_model import Pedido
from app.infrastructure.configs.database_config import Session


class IPedidoRepository(ABC):
    """Interface para operações de Pedido"""

    @abstractmethod
    def create(self, pedido: Pedido, session: Session) -> Pedido:
        pass

    @abstractmethod
    def get_by_id(self, pedido_id: int, session: Session) -> Optional[Pedido]:
        pass

    @abstractmethod
    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[Pedido]:
        pass

    @abstractmethod
    def update(self, pedido: Pedido, session: Session) -> Pedido:
        pass

    @abstractmethod
    def delete(self, pedido_id: int, session: Session) -> bool:
        pass

    @abstractmethod
    def get_by_cliente(self, cliente_id: int, session: Session) -> List[Pedido]:
        pass

    @abstractmethod
    def get_by_status(self, status: str, session: Session) -> List[Pedido]:
        pass

    @abstractmethod
    def get_by_date_range(self, start_date: datetime, end_date: datetime, session: Session) -> List[Pedido]:
        pass

    @abstractmethod
    def get_by_cupom(self, cupom_id: int, session: Session) -> List[Pedido]:
        pass
