"""Use case para listar pedidos recentes"""

from typing import List, Dict, Any
from fastapi import HTTPException, status

from app.application.usecases.use_case import UseCase
from app.domain.models.pedido_model import Pedido
from app.infrastructure.repositories.pedido_repository_interface import IPedidoRepository
from app.infrastructure.repositories.impl.pedido_repository_impl import PedidoRepositoryImpl


class ListPedidosRecentesUseCase(UseCase[Dict[str, Any], List[Dict[str, Any]]]):
    """Use case para listar pedidos recentes"""

    def __init__(self):
        self.pedido_repository: IPedidoRepository = PedidoRepositoryImpl()

    def execute(self, request: Dict[str, Any], session=None) -> List[Dict[str, Any]]:
        """Executa o caso de uso de listagem de pedidos recentes"""
        try:
            days = request.get('days', 7)

            if not isinstance(days, int) or days < 1 or days > 365:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Número de dias deve ser entre 1 e 365"
                )

            pedidos = self.pedido_repository.get_recent_orders(days, session)

            return [self._build_pedido_response(pedido) for pedido in pedidos]

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao listar pedidos recentes: {str(e)}"
            )

    def _build_pedido_response(self, pedido: Pedido) -> Dict[str, Any]:
        """Constrói a resposta do pedido"""
        return {
            "id": pedido.id,
            "id_cliente": pedido.id_cliente,
            "id_cupom": pedido.cupom_id,
            "data_pedido": pedido.data_pedido.isoformat(),
            "status": pedido.status.value,
            "valor_total": float(pedido.valor_total),
            "created_at": pedido.created_at.isoformat(),
            "updated_at": pedido.updated_at.isoformat()
        }
