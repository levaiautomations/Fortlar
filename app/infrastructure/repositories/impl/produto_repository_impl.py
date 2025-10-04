"""Implementação do repository para Produto"""

from typing import Optional, List
from decimal import Decimal

from app.domain.models.produto_model import Produto
from app.infrastructure.configs.database_config import Session
from app.infrastructure.repositories.produto_repository_interface import IProdutoRepository
from app.infrastructure.repositories.base_repository import BaseRepository


class ProdutoRepository(IProdutoRepository, BaseRepository[Produto]):
    """Repository para operações de Produto com CRUD completo"""

    def __init__(self):
        super().__init__(Produto)

    def get_by_codigo(self, codigo: str, session: Session) -> Optional[Produto]:
        """Busca produto por código"""
        return session.query(Produto).filter(Produto.codigo == codigo).first()

    def get_by_categoria(self, categoria_id: int, session: Session) -> List[Produto]:
        """Busca produtos por categoria"""
        return session.query(Produto).filter(Produto.id_categoria == categoria_id).all()

    def get_by_subcategoria(self, subcategoria_id: int, session: Session) -> List[Produto]:
        """Busca produtos por subcategoria"""
        return session.query(Produto).filter(Produto.id_subcategoria == subcategoria_id).all()

    def get_active_products(self, session: Session) -> List[Produto]:
        """Busca produtos ativos"""
        return session.query(Produto).filter(Produto.ativo == True).all()

    def search_by_name(self, name: str, session: Session) -> List[Produto]:
        """Busca produtos por nome"""
        return session.query(Produto).filter(
            Produto.nome.ilike(f"%{name}%")
        ).all()

    def get_by_price_range(self, min_price: Decimal, max_price: Decimal, session: Session) -> List[Produto]:
        """Busca produtos por faixa de preço"""
        return session.query(Produto).filter(
            Produto.valor_base.between(min_price, max_price)
        ).all()

    def search_by_description(self, description: str, session: Session) -> List[Produto]:
        """Busca produtos por descrição"""
        return session.query(Produto).filter(
            Produto.descricao.ilike(f"%{description}%")
        ).all()

    def get_products_with_images(self, session: Session) -> List[Produto]:
        """Busca produtos que possuem imagens"""
        return session.query(Produto).join(Produto.imagens).distinct().all()

    def update_status(self, produto_id: int, ativo: bool, session: Session) -> bool:
        """Atualiza status ativo/inativo do produto"""
        produto = self.get_by_id(produto_id, session)
        if produto:
            produto.ativo = ativo
            session.commit()
            return True
        return False

    def get_products_by_categories(self, categoria_ids: List[int], session: Session) -> List[Produto]:
        """Busca produtos por múltiplas categorias"""
        return session.query(Produto).filter(
            Produto.id_categoria.in_(categoria_ids)
        ).all()
