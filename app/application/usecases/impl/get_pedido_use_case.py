"""Use case para buscar pedido por ID"""

from typing import Dict, Any, Optional
from fastapi import HTTPException, status

from app.application.usecases.use_case import UseCase
from app.domain.models.pedido_model import Pedido
from app.infrastructure.repositories.pedido_repository_interface import IPedidoRepositoryImpl
from app.infrastructure.repositories.impl.pedido_repository_impl import PedidoRepositoryImplImpl


class GetPedidoUseCase(UseCase[Dict[str, Any], Dict[str, Any]]):
    """Use case para buscar pedido por ID"""

    def __init__(self):
        self.pedido_repository: IPedidoRepositoryImpl = PedidoRepositoryImplImpl()

    def execute(self, request: Dict[str, Any], session=None) -> Dict[str, Any]:
        """Executa o caso de uso de busca de pedido"""
        try:
            pedido_id = request.get('pedido_id')
            include_items = request.get('include_items', False)

            if not pedido_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ID do pedido é obrigatório"
                )

            # Busca o pedido
            if include_items:
                pedido = self.pedido_repository.get_orders_with_items(pedido_id, session)
            else:
                pedido = self.pedido_repository.get_by_id(pedido_id, session)

            if not pedido:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pedido não encontrado"
                )

            return self._build_pedido_response(pedido, include_items)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar pedido: {str(e)}"
            )

    def _build_pedido_response(self, pedido: Pedido, include_items: bool = False) -> Dict[str, Any]:
        """Constrói a resposta do pedido"""
        result = {
            "id": pedido.id,
            "id_cliente": pedido.id_cliente,
            "id_cupom": pedido.cupom_id,
            "data_pedido": pedido.data_pedido.isoformat(),
            "status": pedido.status.value,
            "valor_total": float(pedido.valor_total),
            "created_at": pedido.created_at.isoformat(),
            "updated_at": pedido.updated_at.isoformat()
        }

        if include_items and hasattr(pedido, 'itens'):
            result["itens"] = [
                {
                    "id": item.id,
                    "id_produto": item.id_produto,
                    "quantidade": item.quantidade,
                    "preco_unitario": float(item.preco_unitario),
                    "subtotal": float(item.subtotal)
                }
                for item in pedido.itens
            ]

        return result
