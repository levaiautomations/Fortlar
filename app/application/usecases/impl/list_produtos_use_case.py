"""Use case para listar produtos"""

from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status

from app.application.usecases.use_case import UseCase
from app.domain.models.product_model import Product
from app.infrastructure.repositories.product_repository_interface import IProductRepository
from app.infrastructure.repositories.impl.product_repository_impl import ProductRepositoryImpl


class ListProductsUseCase(UseCase[Dict[str, Any], List[Dict[str, Any]]]):
    """Use case para listar produtos"""

    def __init__(self):
        self.product_repository: IProductRepository = ProductRepositoryImpl()

    def execute(self, request: Dict[str, Any], session=None) -> List[Dict[str, Any]]:
        """Executa o caso de uso de listagem de produtos com filtros consolidados"""
        try:
            skip = request.get('skip', 0)
            limit = request.get('limit')  # None se não for passado (retorna todos)
            active_only = request.get('active_only', True)
            categoria_id = request.get('id_category') or request.get('categoria_id')
            subcategoria_id = request.get('id_subcategory') or request.get('subcategoria_id')
            order_price = request.get('order_price')  # 'ASC' ou 'DESC'
            search_name = request.get('search_name')
            min_price = request.get('min_price')
            max_price = request.get('max_price')

            # Busca produtos usando o método consolidado com filtros
            if search_name:
                products = self.product_repository.search_by_name(search_name, session)
            elif min_price is not None and max_price is not None:
                from decimal import Decimal
                products = self.product_repository.get_by_price_range(
                    Decimal(str(min_price)), 
                    Decimal(str(max_price)), 
                    session
                )
            else:
                # Usa método consolidado que suporta todos os filtros
                products = self.product_repository.get_all_with_filters(
                    session=session,
                    categoria_id=categoria_id,
                    subcategoria_id=subcategoria_id,
                    active_only=active_only,
                    order_by_price=order_price,
                    skip=skip,
                    limit=limit
                )

            # Converte para DTOs de resposta
            return [self._build_product_response(product) for product in products]

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao listar produtos: {str(e)}"
            )

    def _build_product_response(self, product: Product) -> Dict[str, Any]:
        """Constrói a resposta do product"""
        # Converte cod_kit para string ou None (pode vir como int do banco)
        cod_kit_str = None
        if product.cod_kit is not None:
            cod_kit_str = str(product.cod_kit)
        
        return {
            'id_produto': product.id_produto,
            'codigo': product.codigo,
            'nome': product.nome,
            'descricao': product.descricao,
            'quantidade': product.quantidade,
            'cod_kit': cod_kit_str,
            'id_categoria': product.id_categoria,
            'id_subcategoria': product.id_subcategoria,
            'valor_base': float(product.valor_base),
            'ativo': product.ativo,
            'created_at': product.created_at.isoformat(),
            'updated_at': product.updated_at.isoformat() if product.updated_at else None,
            'categoria': product.categoria.nome if product.categoria else None,
            'subcategoria': product.subcategoria.nome if product.subcategoria else None,
            'imagens': [img.url for img in product.imagens] if product.imagens else []
        }
