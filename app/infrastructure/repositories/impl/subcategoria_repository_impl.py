"""Implementação do repository para Subcategoria"""

from typing import Optional, List

from app.domain.models.subcategoria_model import Subcategoria
from app.infrastructure.configs.database_config import Session
from app.infrastructure.repositories.subcategoria_repository_interface import ISubcategoriaRepository
from app.infrastructure.repositories.base_repository import BaseRepository


class SubcategoriaRepositoryImpl(ISubcategoriaRepository, BaseRepository[Subcategoria]):
    """Repository para operações de Subcategoria com CRUD completo"""

    def __init__(self):
        super().__init__(Subcategoria)

    # Implementação dos métodos abstratos do ISubcategoriaRepository
    def create(self, subcategoria: Subcategoria, session: Session) -> Subcategoria:
        """Cria uma nova subcategoria"""
        return super().create(subcategoria, session)

    def get_by_id(self, subcategoria_id: int, session: Session) -> Optional[Subcategoria]:
        """Busca subcategoria por ID"""
        return super().get_by_id(subcategoria_id, session)

    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[Subcategoria]:
        """Lista todas as subcategorias"""
        return super().get_all(session, skip, limit)

    def update(self, subcategoria: Subcategoria, session: Session) -> Subcategoria:
        """Atualiza uma subcategoria"""
        return super().update(subcategoria, session)

    def delete(self, subcategoria_id: int, session: Session) -> bool:
        """Deleta uma subcategoria"""
        return super().delete(subcategoria_id, session)

    def get_by_name(self, name: str, session: Session) -> Optional[Subcategoria]:
        """Busca subcategoria por nome exato"""
        return session.query(Subcategoria).filter(Subcategoria.nome == name).first()

    def get_by_categoria(self, categoria_id: int, session: Session) -> List[Subcategoria]:
        """Busca subcategorias por categoria"""
        return session.query(Subcategoria).filter(
            Subcategoria.id_categoria == categoria_id
        ).all()

    def search_by_name(self, name: str, session: Session) -> List[Subcategoria]:
        """Busca subcategorias por nome (busca parcial)"""
        return session.query(Subcategoria).filter(
            Subcategoria.nome.ilike(f"%{name}%")
        ).all()

    def exists_by_name(self, name: str, session: Session) -> bool:
        """Verifica se subcategoria existe por nome"""
        return session.query(Subcategoria).filter(Subcategoria.nome == name).first() is not None
