"""Implementação do repository para Product"""

from typing import Optional, List
from decimal import Decimal

from app.domain.models.product_model import Product
from app.infrastructure.configs.database_config import Session
from app.infrastructure.repositories.product_repository_interface import IProductRepository


class ProductRepositoryImpl(IProductRepository):
    """Repository para operações de Product com CRUD completo"""

    # Implementação dos métodos abstratos do IProductRepository
    def create(self, product: Product, session: Session) -> Product:
        """Cria um novo product"""
        session.add(product)
        session.flush()
        return product

    def get_by_id(self, product_id: int, session: Session) -> Optional[Product]:
        """Busca product por ID"""
        return session.query(Product).filter(Product.id_produto == product_id).first()

    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        """Lista todos os products"""
        return session.query(Product).offset(skip).limit(limit).all()

    def update(self, product: Product, session: Session) -> Product:
        """Atualiza um product"""
        session.merge(product)
        session.flush()
        return product

    def delete(self, product_id: int, session: Session) -> bool:
        """Deleta um product"""
        product = self.get_by_id(product_id, session)
        if product:
            session.delete(product)
            session.flush()
            return True
        return False

    def get_by_codigo(self, codigo: str, session: Session) -> Optional[Product]:
        """Busca product por código"""
        return session.query(Product).filter(Product.codigo == codigo).first()

    def get_by_categoria(self, categoria_id: int, session: Session) -> List[Product]:
        """Busca products por categoria"""
        return session.query(Product).filter(Product.id_categoria == categoria_id).all()

    def get_by_subcategoria(self, subcategoria_id: int, session: Session) -> List[Product]:
        """Busca products por subcategoria"""
        return session.query(Product).filter(Product.id_subcategoria == subcategoria_id).all()

    def get_active_products(self, session: Session) -> List[Product]:
        """Busca products ativos"""
        return session.query(Product).filter(Product.ativo == True).all()

    def search_by_name(self, name: str, session: Session) -> List[Product]:
        """Busca products por nome"""
        return session.query(Product).filter(
            Product.nome.ilike(f"%{name}%")
        ).all()

    def get_by_price_range(self, min_price: Decimal, max_price: Decimal, session: Session) -> List[Product]:
        """Busca products por faixa de preço"""
        return session.query(Product).filter(
            Product.valor_base.between(min_price, max_price)
        ).all()

    def search_by_description(self, description: str, session: Session) -> List[Product]:
        """Busca products por descrição"""
        return session.query(Product).filter(
            Product.descricao.ilike(f"%{description}%")
        ).all()

    def get_products_with_images(self, session: Session) -> List[Product]:
        """Busca products que possuem imagens"""
        return session.query(Product).join(Product.imagens).distinct().all()

    def update_status(self, product_id: int, ativo: bool, session: Session) -> bool:
        """Atualiza status ativo/inativo do product"""
        product = self.get_by_id(product_id, session)
        if product:
            product.ativo = ativo
            session.commit()
            return True
        return False

    def get_products_by_categories(self, categoria_ids: List[int], session: Session) -> List[Product]:
        """Busca products por múltiplas categorias"""
        return session.query(Product).filter(
            Product.id_categoria.in_(categoria_ids)
        ).all()

    def get_all_with_filters(
        self, 
        session: Session,
        categoria_id: Optional[int] = None,
        subcategoria_id: Optional[int] = None,
        active_only: bool = True,
        order_by_price: Optional[str] = None,
        skip: int = 0,
        limit: Optional[int] = None
    ) -> List[Product]:
        """Busca produtos com filtros e ordenação. Se limit=None, retorna todos os registros"""
        from sqlalchemy import asc, desc
        
        query = session.query(Product)
        
        # Aplica filtros
        if active_only:
            query = query.filter(Product.ativo == True)
        
        if categoria_id is not None:
            query = query.filter(Product.id_categoria == categoria_id)
        
        if subcategoria_id is not None:
            query = query.filter(Product.id_subcategoria == subcategoria_id)
        
        # Aplica ordenação por preço
        if order_by_price:
            if order_by_price.upper() == 'ASC':
                query = query.order_by(asc(Product.valor_base))
            elif order_by_price.upper() == 'DESC':
                query = query.order_by(desc(Product.valor_base))
        else:
            # Ordenação padrão por ID
            query = query.order_by(Product.id_produto)
        
        # Aplica skip
        if skip > 0:
            query = query.offset(skip)
        
        # Aplica limit apenas se fornecido
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
