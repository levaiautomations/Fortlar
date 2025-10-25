from typing import Optional, List
from decimal import Decimal

from app.domain.models.item_pedido_model import ItemPedido
from app.infrastructure.configs.database_config import Session
from app.infrastructure.repositories.item_pedido_repository_interface import IItemPedidoRepository
from app.infrastructure.repositories.base_repository import BaseRepository


class ItemPedidoRepositoryImpl(IItemPedidoRepository, BaseRepository[ItemPedido]):
    """Repository para operações de ItemPedido com CRUD completo"""

    def __init__(self):
        super().__init__(ItemPedido)

    def create(self, item_pedido: ItemPedido, session: Session) -> ItemPedido:
        """Cria um novo item de pedido"""
        session.add(item_pedido)
        session.flush()
        return item_pedido

    def get_by_id(self, item_id: int, session: Session) -> Optional[ItemPedido]:
        """Busca item de pedido por ID"""
        return session.query(ItemPedido).filter(ItemPedido.id == item_id).first()

    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[ItemPedido]:
        """Lista todos os itens de pedido"""
        return session.query(ItemPedido).offset(skip).limit(limit).all()

    def update(self, item_pedido: ItemPedido, session: Session) -> ItemPedido:
        """Atualiza um item de pedido"""
        session.merge(item_pedido)
        session.flush()
        return item_pedido

    def delete(self, item_id: int, session: Session) -> bool:
        """Deleta um item de pedido"""
        item = self.get_by_id(item_id, session)
        if item:
            session.delete(item)
            session.flush()
            return True
        return False

    def get_by_pedido_id(self, pedido_id: int, session: Session) -> List[ItemPedido]:
        """Busca itens por ID do pedido"""
        return session.query(ItemPedido).filter(ItemPedido.id_pedido == pedido_id).all()

    def get_by_produto_id(self, produto_id: int, session: Session) -> List[ItemPedido]:
        """Busca itens por ID do produto"""
        return session.query(ItemPedido).filter(ItemPedido.id_produto == produto_id).all()

    def get_total_by_pedido(self, pedido_id: int, session: Session) -> float:
        """Calcula total dos itens de um pedido"""
        from sqlalchemy import func
        result = session.query(func.sum(ItemPedido.subtotal)).filter(
            ItemPedido.id_pedido == pedido_id
        ).scalar()
        return float(result) if result else 0.0

    def get_quantity_by_produto(self, produto_id: int, session: Session) -> int:
        """Calcula quantidade total vendida de um produto"""
        from sqlalchemy import func
        result = session.query(func.sum(ItemPedido.quantidade)).filter(
            ItemPedido.id_produto == produto_id
        ).scalar()
        return int(result) if result else 0
