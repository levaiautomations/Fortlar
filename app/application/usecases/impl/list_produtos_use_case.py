"""Use case para listar produtos"""

from typing import List, Dict, Any
from fastapi import HTTPException, status

from app.application.usecases.use_case import UseCase
from app.domain.models.produto_model import Produto
from app.infrastructure.repositories.produto_repository_interface import IProdutoRepository


class ListProdutosUseCase(UseCase[Dict[str, Any], List[Dict[str, Any]]]):
    """Use case para listar produtos"""

    def __init__(self, produto_repository: IProdutoRepository):
        self.produto_repository = produto_repository

    def execute(self, request: Dict[str, Any], session=None) -> List[Dict[str, Any]]:
        """Executa o caso de uso de listagem de produtos"""
        try:
            skip = request.get('skip', 0)
            limit = request.get('limit', 100)
            active_only = request.get('active_only', True)
            categoria_id = request.get('categoria_id')
            subcategoria_id = request.get('subcategoria_id')
            search_name = request.get('search_name')
            min_price = request.get('min_price')
            max_price = request.get('max_price')

            # Busca produtos baseado nos filtros
            if search_name:
                produtos = self.produto_repository.search_by_name(search_name, session)
            elif categoria_id:
                produtos = self.produto_repository.get_by_categoria(categoria_id, session)
            elif subcategoria_id:
                produtos = self.produto_repository.get_by_subcategoria(subcategoria_id, session)
            elif min_price is not None and max_price is not None:
                from decimal import Decimal
                produtos = self.produto_repository.get_by_price_range(
                    Decimal(str(min_price)), 
                    Decimal(str(max_price)), 
                    session
                )
            elif active_only:
                produtos = self.produto_repository.get_active_products(session)
            else:
                produtos = self.produto_repository.get_all(session, skip, limit)

            # Converte para DTOs de resposta
            return [self._build_produto_response(produto) for produto in produtos]

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao listar produtos: {str(e)}"
            )

    def _build_produto_response(self, produto: Produto) -> Dict[str, Any]:
        """Constrói a resposta do produto"""
        return {
            'id': produto.id,
            'codigo': produto.codigo,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'id_categoria': produto.id_categoria,
            'id_subcategoria': produto.id_subcategoria,
            'valor_base': float(produto.valor_base),
            'ativo': produto.ativo,
            'created_at': produto.created_at.isoformat(),
            'updated_at': produto.updated_at.isoformat(),
            'categoria': produto.categoria.nome if produto.categoria else None,
            'subcategoria': produto.subcategoria.nome if produto.subcategoria else None
        }
