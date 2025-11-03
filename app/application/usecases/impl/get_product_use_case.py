"""Use case para buscar produto por ID"""

from typing import Dict, Any, Optional
from fastapi import HTTPException, status

from app.application.usecases.use_case import UseCase
from app.domain.models.product_model import Product
from app.infrastructure.repositories.product_repository_interface import IProductRepository
from app.infrastructure.repositories.impl.product_repository_impl import ProductRepositoryImpl


class GetProductUseCase(UseCase[int, Dict[str, Any]]):
    """Use case para buscar produto por ID"""

    def __init__(self):
        self.product_repository: IProductRepository = ProductRepositoryImpl()

    def execute(self, product_id: int, session=None) -> Dict[str, Any]:
        """Executa o caso de uso de busca de produto por ID"""
        try:
            # Busca o produto
            product = self.product_repository.get_by_id(product_id, session)

            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Produto não encontrado"
                )

            return self._build_product_response(product)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar produto: {str(e)}"
            )

    def _build_product_response(self, product: Product) -> Dict[str, Any]:
        """Constrói a resposta do produto"""
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

