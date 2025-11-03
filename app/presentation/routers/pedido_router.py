"""Router para operações de Pedidos - Refatorado com Clean Architecture e SOLID"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from typing import List
from loguru import logger

# Use Cases
from app.application.usecases.impl.list_pedidos_use_case import ListPedidosUseCase
from app.application.usecases.impl.get_pedido_use_case import GetPedidoUseCase
from app.application.usecases.impl.list_pedidos_recentes_use_case import ListPedidosRecentesUseCase

# Services
from app.application.service.email_service import EmailService
from app.application.service.email.template.pedido_template import pedido_html

# Repositories
from app.infrastructure.repositories.impl.company_repository_impl import CompanyRepositoryImpl
from app.infrastructure.repositories.impl.product_repository_impl import ProductRepositoryImpl

# Configs
from app.infrastructure.configs.database_config import Session
from app.infrastructure.configs.session_config import get_session
from app.infrastructure.configs.security_config import verify_user_permission
from app.presentation.routers.request.pedido_request import (
    ListPedidosRequest,
    GetPedidoRequest,
    ListPedidosByClienteRequest,
    ListPedidosByStatusRequest,
    ListPedidosRecentesRequest,
    EnvioPedidoRequest
)
from app.presentation.routers.response.pedido_response import (
    PedidoResponse,
    ListPedidosResponse
)

pedido_router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"],
    responses={
        404: {"description": "Pedido não encontrado"},
        422: {"description": "Dados inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)


# Dependency Injection Functions removidas - usando padrão simples


@pedido_router.get(
    "/",
    summary="Listar pedidos",
    description="Lista todos os pedidos com filtros opcionais",
    response_model=List[PedidoResponse]
)
async def list_pedidos(
    request: ListPedidosRequest = Depends(),
    session: Session = Depends(get_session),
    current_user = Depends(verify_user_permission())
) -> List[PedidoResponse]:
    """
    Lista pedidos com filtros opcionais.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Open/Closed: Extensível via novos filtros sem modificar código existente
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: ListPedidosUseCase = ListPedidosUseCase()
        pedidos_data = use_case.execute(request.dict(), session)
        return [PedidoResponse(**pedido) for pedido in pedidos_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {str(e)}")


@pedido_router.get(
    "/{pedido_id}",
    summary="Buscar pedido por ID",
    description="Busca um pedido específico pelo ID",
    response_model=PedidoResponse
)
async def get_pedido(
    pedido_id: int = Path(..., description="ID do pedido"),
    include_items: bool = Query(False, description="Incluir itens do pedido"),
    session: Session = Depends(get_session),
    current_user = Depends(verify_user_permission())
) -> PedidoResponse:
    """
    Busca pedido por ID.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: GetPedidoUseCase = GetPedidoUseCase()
        request = GetPedidoRequest(pedido_id=pedido_id, include_items=include_items)
        pedido_data = use_case.execute(request.dict(), session)
        return PedidoResponse(**pedido_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pedido: {str(e)}")


@pedido_router.get(
    "/cliente/{cliente_id}",
    summary="Listar pedidos do cliente",
    description="Lista todos os pedidos de um cliente específico",
    response_model=List[PedidoResponse]
)
async def list_pedidos_by_cliente(
    cliente_id: int = Path(..., description="ID do cliente"),
    session: Session = Depends(get_session)
) -> List[PedidoResponse]:
    """
    Lista pedidos de um cliente específico.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: ListPedidosUseCase = ListPedidosUseCase()
        request = ListPedidosByClienteRequest(cliente_id=cliente_id)
        pedidos_data = use_case.execute(request.dict(), session)
        return [PedidoResponse(**pedido) for pedido in pedidos_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos do cliente: {str(e)}")


@pedido_router.get(
    "/status/{status}",
    summary="Listar pedidos por status",
    description="Lista pedidos com um status específico",
    response_model=List[PedidoResponse]
)
async def list_pedidos_by_status(
    status: str = Path(..., description="Status do pedido"),
    session: Session = Depends(get_session)
) -> List[PedidoResponse]:
    """
    Lista pedidos por status.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: ListPedidosUseCase = ListPedidosUseCase()
        request = ListPedidosByStatusRequest(status=status)
        pedidos_data = use_case.execute(request.dict(), session)
        return [PedidoResponse(**pedido) for pedido in pedidos_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos por status: {str(e)}")


@pedido_router.get(
    "/recentes",
    summary="Listar pedidos recentes",
    description="Lista pedidos dos últimos X dias",
    response_model=List[PedidoResponse]
)
async def list_pedidos_recentes(
    days: int = Query(7, ge=1, le=365, description="Número de dias"),
    session: Session = Depends(get_session)
) -> List[PedidoResponse]:
    """
    Lista pedidos recentes.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: ListPedidosRecentesUseCase = ListPedidosRecentesUseCase()
        request = ListPedidosRecentesRequest(days=days)
        pedidos_data = use_case.execute(request.dict(), session)
        return [PedidoResponse(**pedido) for pedido in pedidos_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos recentes: {str(e)}")


@pedido_router.post(
    "/enviar",
    summary="Enviar pedido por email",
    description="Recebe o carrinho e envia um email formatado em HTML para a empresa com os detalhes do pedido",
    response_class=JSONResponse
)
async def enviar_pedido(
    request: EnvioPedidoRequest,
    session: Session = Depends(get_session),
    current_user = Depends(verify_user_permission())
):
    """
    Envia pedido por email.
    
    Recebe o carrinho com itens (produtos, quantidades, preços) e a forma de pagamento,
    busca as informações dos produtos, gera um HTML formatado e envia por email para a empresa.
    """
    try:
        logger.info(f"=== Enviando pedido para cliente {request.id_cliente} ===")
        
        # Inicializa repositories e services
        company_repo = CompanyRepositoryImpl()
        product_repo = ProductRepositoryImpl()
        email_service = EmailService()
        
        # Busca empresa com contatos
        company = company_repo.get_with_relations(request.id_cliente, session)
        if not company:
            raise HTTPException(status_code=404, detail=f"Empresa com ID {request.id_cliente} não encontrada")
        
        # Verifica se empresa tem email cadastrado
        if not company.contatos or len(company.contatos) == 0:
            raise HTTPException(
                status_code=400, 
                detail="Empresa não possui contato com email cadastrado"
            )
        
        # Pega o primeiro email dos contatos
        email_empresa = company.contatos[0].email
        if not email_empresa:
            raise HTTPException(
                status_code=400,
                detail="Empresa não possui email cadastrado nos contatos"
            )
        
        # Busca produtos e monta lista formatada
        itens_formatados = []
        valor_total = 0.0
        
        for item_carrinho in request.itens:
            # Busca produto
            produto = product_repo.get_by_id(item_carrinho.id_produto, session)
            if not produto:
                logger.warning(f"Produto com ID {item_carrinho.id_produto} não encontrado")
                continue
            
            # Calcula subtotal
            subtotal = float(item_carrinho.preco_unitario) * item_carrinho.quantidade
            valor_total += subtotal
            
            # Formata item
            itens_formatados.append({
                'nome': produto.nome,
                'quantidade': item_carrinho.quantidade,
                'preco_unitario': float(item_carrinho.preco_unitario),
                'subtotal': subtotal
            })
        
        if not itens_formatados:
            raise HTTPException(
                status_code=400,
                detail="Nenhum produto válido encontrado no carrinho"
            )
        
        # Gera HTML do pedido
        html_email = pedido_html(
            itens=itens_formatados,
            valor_total=valor_total,
            forma_pagamento=request.forma_pagamento
        )
        
        # Envia email
        subject = f"Novo Pedido - Fortlar - Total: R$ {valor_total:.2f}"
        email_service.send_email(email_empresa, html_email, subject)
        
        logger.info(f"✅ Email de pedido enviado com sucesso para {email_empresa}")
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Pedido enviado por email com sucesso",
                "email_enviado": email_empresa,
                "valor_total": valor_total,
                "quantidade_itens": len(itens_formatados)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao enviar pedido por email: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao enviar pedido por email: {str(e)}")
