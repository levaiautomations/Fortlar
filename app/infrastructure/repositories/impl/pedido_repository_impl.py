"""Implementação do repository para Pedido"""

from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from app.domain.models.pedido_model import Pedido, PedidoStatusEnum
from app.infrastructure.configs.database_config import Session
from app.infrastructure.repositories.pedido_repository_interface import IPedidoRepository
from app.infrastructure.repositories.base_repository import BaseRepository


class PedidoRepository(IPedidoRepository, BaseRepository[Pedido]):
    """Repository para operações de Pedido com CRUD completo"""

    def __init__(self):
        super().__init__(Pedido)

    def get_by_cliente(self, cliente_id: int, session: Session) -> List[Pedido]:
        """Busca pedidos por cliente"""
        return session.query(Pedido).filter(Pedido.id_cliente == cliente_id).all()

    def get_by_status(self, status: PedidoStatusEnum, session: Session) -> List[Pedido]:
        """Busca pedidos por status"""
        return session.query(Pedido).filter(Pedido.status == status).all()

    def get_by_date_range(self, start_date: datetime, end_date: datetime, session: Session) -> List[Pedido]:
        """Busca pedidos por intervalo de datas"""
        return session.query(Pedido).filter(
            Pedido.data_pedido.between(start_date, end_date)
        ).all()

    def get_by_cupom(self, cupom_id: int, session: Session) -> List[Pedido]:
        """Busca pedidos por cupom"""
        return session.query(Pedido).filter(Pedido.cupom_id == cupom_id).all()

    def get_pending_orders(self, session: Session) -> List[Pedido]:
        """Busca pedidos pendentes"""
        return session.query(Pedido).filter(
            Pedido.status == PedidoStatusEnum.PENDENTE
        ).all()

    def get_orders_by_value_range(self, min_value: Decimal, max_value: Decimal, session: Session) -> List[Pedido]:
        """Busca pedidos por faixa de valor"""
        return session.query(Pedido).filter(
            Pedido.valor_total.between(min_value, max_value)
        ).all()

    def get_recent_orders(self, days: int, session: Session) -> List[Pedido]:
        """Busca pedidos recentes (últimos X dias)"""
        from datetime import timedelta
        start_date = datetime.now() - timedelta(days=days)
        return session.query(Pedido).filter(
            Pedido.data_pedido >= start_date
        ).all()

    def update_status(self, pedido_id: int, status: PedidoStatusEnum, session: Session) -> bool:
        """Atualiza status do pedido"""
        pedido = self.get_by_id(pedido_id, session)
        if pedido:
            pedido.status = status
            session.commit()
            return True
        return False

    def get_orders_with_items(self, pedido_id: int, session: Session) -> Optional[Pedido]:
        """Busca pedido com itens"""
        from sqlalchemy.orm import joinedload
        return session.query(Pedido).options(
            joinedload(Pedido.itens)
        ).filter(Pedido.id == pedido_id).first()
