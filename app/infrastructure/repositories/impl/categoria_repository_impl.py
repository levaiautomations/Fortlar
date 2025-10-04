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

    # Implementação dos métodos abstratos do ICategoriaRepository
    def create(self, categoria: Categoria, session: Session) -> Categoria:
        """Cria uma nova categoria"""
        return super().create(categoria, session)

    def get_by_id(self, categoria_id: int, session: Session) -> Optional[Categoria]:
        """Busca categoria por ID"""
        return super().get_by_id(categoria_id, session)

    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[Categoria]:
        """Lista todas as categorias"""
        return super().get_all(session, skip, limit)

    def update(self, categoria: Categoria, session: Session) -> Categoria:
        """Atualiza uma categoria"""
        return super().update(categoria, session)

    def delete(self, categoria_id: int, session: Session) -> bool:
        """Deleta uma categoria"""
        return super().delete(categoria_id, session)

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
