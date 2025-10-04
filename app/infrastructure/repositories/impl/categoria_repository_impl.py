"""Implementação do repository para Categoria"""

from typing import Optional, List

from app.domain.models.categoria_model import Categoria
from app.infrastructure.configs.database_config import Session
from app.infrastructure.repositories.categoria_repository_interface import ICategoriaRepository
from app.infrastructure.repositories.base_repository import BaseRepository


class CategoriaRepository(ICategoriaRepository, BaseRepository[Categoria]):
    """Repository para operações de Categoria com CRUD completo"""

    def __init__(self):
        super().__init__(Categoria)

    def get_by_name(self, name: str, session: Session) -> Optional[Categoria]:
        """Busca categoria por nome exato"""
        return session.query(Categoria).filter(Categoria.nome == name).first()

    def search_by_name(self, name: str, session: Session) -> List[Categoria]:
        """Busca categorias por nome (busca parcial)"""
        return session.query(Categoria).filter(
            Categoria.nome.ilike(f"%{name}%")
        ).all()

    def exists_by_name(self, name: str, session: Session) -> bool:
        """Verifica se categoria existe por nome"""
        return session.query(Categoria).filter(Categoria.nome == name).first() is not None

    def get_categories_with_products(self, session: Session) -> List[Categoria]:
        """Busca categorias que possuem produtos"""
        return session.query(Categoria).join(Categoria.produtos).distinct().all()

    def get_categories_with_subcategories(self, session: Session) -> List[Categoria]:
        """Busca categorias que possuem subcategorias"""
        return session.query(Categoria).join(Categoria.subcategorias).distinct().all()
