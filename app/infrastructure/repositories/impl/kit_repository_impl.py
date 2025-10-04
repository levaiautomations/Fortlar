"""Implementação do repository para Kit"""

from typing import Optional, List
from decimal import Decimal

from app.domain.models.kit_model import Kit
from app.infrastructure.configs.database_config import Session
from app.infrastructure.repositories.kit_repository_interface import IKitRepository
from app.infrastructure.repositories.base_repository import BaseRepository


class KitRepository(IKitRepository, BaseRepository[Kit]):
    """Repository para operações de Kit com CRUD completo"""

    def __init__(self):
        super().__init__(Kit)

    def get_by_codigo(self, codigo: str, session: Session) -> Optional[Kit]:
        """Busca kit por código"""
        return session.query(Kit).filter(Kit.codigo == codigo).first()

    def get_active_kits(self, session: Session) -> List[Kit]:
        """Busca kits ativos"""
        return session.query(Kit).filter(Kit.ativo == True).all()

    def search_by_name(self, name: str, session: Session) -> List[Kit]:
        """Busca kits por nome"""
        return session.query(Kit).filter(
            Kit.nome.ilike(f"%{name}%")
        ).all()

    def get_by_categoria(self, categoria: str, session: Session) -> List[Kit]:
        """Busca kits por categoria"""
        return session.query(Kit).filter(
            Kit.categoria.ilike(f"%{categoria}%")
        ).all()

    def get_kits_with_products(self, session: Session) -> List[Kit]:
        """Busca kits que possuem produtos"""
        return session.query(Kit).join(Kit.produtos).distinct().all()

    def search_by_description(self, description: str, session: Session) -> List[Kit]:
        """Busca kits por descrição"""
        return session.query(Kit).filter(
            Kit.descricao.ilike(f"%{description}%")
        ).all()

    def get_by_price_range(self, min_price: Decimal, max_price: Decimal, session: Session) -> List[Kit]:
        """Busca kits por faixa de preço"""
        return session.query(Kit).filter(
            Kit.valor_total.between(min_price, max_price)
        ).all()

    def get_kits_with_images(self, session: Session) -> List[Kit]:
        """Busca kits que possuem imagens"""
        return session.query(Kit).join(Kit.imagens).distinct().all()

    def update_status(self, kit_id: int, ativo: bool, session: Session) -> bool:
        """Atualiza status ativo/inativo do kit"""
        kit = self.get_by_id(kit_id, session)
        if kit:
            kit.ativo = ativo
            session.commit()
            return True
        return False
