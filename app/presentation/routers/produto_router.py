"""Router para operações de Produtos - Refatorado com Clean Architecture e SOLID"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List, Optional
import os
import tempfile
import io
import pandas as pd

# Use Cases
from app.application.usecases.impl.list_produtos_use_case import ListProdutosUseCase
from app.application.usecases.impl.bulk_create_produtos_use_case import BulkCreateProdutosUseCase

# Services
from app.application.service.excel_service import ExcelService

# Repositories
from app.infrastructure.repositories.impl.produto_repository_impl import ProdutoRepository
from app.infrastructure.repositories.impl.categoria_repository_impl import CategoriaRepository
from app.infrastructure.repositories.impl.subcategoria_repository_impl import SubcategoriaRepository

# Configs
from app.infrastructure.configs.database_config import Session
from app.infrastructure.configs.session_config import get_session
from app.infrastructure.configs.security_config import verify_user_permission
from app.presentation.routers.request.produto_request import (
    ListProdutosRequest,
    ListProdutosByCategoriaRequest,
    ListProdutosBySubcategoriaRequest,
    SearchProdutosRequest,
    ListProdutosByPriceRangeRequest
)
from app.presentation.routers.request.excel_request import (
    ExcelUploadRequest,
    ExcelValidationResponse,
    BulkCreateResponse
)
from app.presentation.routers.response.produto_response import (
    ProdutoResponse,
    ListProdutosResponse
)

produto_router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"],
    responses={
        404: {"description": "Produto não encontrado"},
        422: {"description": "Dados inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)


# Dependency Injection Functions removidas - usando padrão simples


@produto_router.get(
    "/",
    summary="Listar produtos",
    description="Lista todos os produtos com filtros opcionais",
    response_model=List[ProdutoResponse]
)
async def list_produtos(
    request: ListProdutosRequest = Depends(),
    session: Session = Depends(get_session),
    current_user = Depends(verify_user_permission())
) -> List[ProdutoResponse]:
    """
    Lista produtos com filtros opcionais.
    
    **Autenticação necessária**: Bearer Token JWT
    
    Args:
        token (str): Token Bearer de autenticação no header Authorization
        
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Open/Closed: Extensível via novos filtros sem modificar código existente
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: ListProdutosUseCase = ListProdutosUseCase()
        produtos_data = use_case.execute(request.dict(), session)
        return [ProdutoResponse(**produto) for produto in produtos_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")


@produto_router.get(
    "/categoria/{categoria_id}",
    summary="Listar produtos por categoria",
    description="Lista produtos de uma categoria específica",
    response_model=List[ProdutoResponse]
)
async def list_produtos_by_categoria(
    categoria_id: int = Path(..., description="ID da categoria"),
    active_only: bool = Query(True, description="Filtrar apenas produtos ativos"),
    session: Session = Depends(get_session),
    current_user = Depends(verify_user_permission())
) -> List[ProdutoResponse]:
    """
    Lista produtos por categoria.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: ListProdutosUseCase = ListProdutosUseCase()
        request = ListProdutosByCategoriaRequest(categoria_id=categoria_id, active_only=active_only)
        produtos_data = use_case.execute(request.dict(), session)
        return [ProdutoResponse(**produto) for produto in produtos_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos por categoria: {str(e)}")


@produto_router.get(
    "/subcategoria/{subcategoria_id}",
    summary="Listar produtos por subcategoria",
    description="Lista produtos de uma subcategoria específica",
    response_model=List[ProdutoResponse]
)
async def list_produtos_by_subcategoria(
    subcategoria_id: int = Path(..., description="ID da subcategoria"),
    active_only: bool = Query(True, description="Filtrar apenas produtos ativos"),
    session: Session = Depends(get_session),
    current_user = Depends(verify_user_permission())
) -> List[ProdutoResponse]:
    """
    Lista produtos por subcategoria.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: ListProdutosUseCase = ListProdutosUseCase()
        request = ListProdutosBySubcategoriaRequest(subcategoria_id=subcategoria_id, active_only=active_only)
        produtos_data = use_case.execute(request.dict(), session)
        return [ProdutoResponse(**produto) for produto in produtos_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos por subcategoria: {str(e)}")


@produto_router.get(
    "/search",
    summary="Buscar produtos",
    description="Busca produtos por nome ou descrição",
    response_model=List[ProdutoResponse]
)
async def search_produtos(
    q: str = Query(..., description="Termo de busca"),
    active_only: bool = Query(True, description="Filtrar apenas produtos ativos"),
    session: Session = Depends(get_session),
    current_user = Depends(verify_user_permission())
) -> List[ProdutoResponse]:
    """
    Busca produtos por termo.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: ListProdutosUseCase = ListProdutosUseCase()
        request = SearchProdutosRequest(q=q, active_only=active_only)
        produtos_data = use_case.execute(request.dict(), session)
        return [ProdutoResponse(**produto) for produto in produtos_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produtos: {str(e)}")


@produto_router.get(
    "/price-range",
    summary="Listar produtos por faixa de preço",
    description="Lista produtos dentro de uma faixa de preço",
    response_model=List[ProdutoResponse]
)
async def list_produtos_by_price_range(
    min_price: float = Query(..., ge=0, description="Preço mínimo"),
    max_price: float = Query(..., ge=0, description="Preço máximo"),
    active_only: bool = Query(True, description="Filtrar apenas produtos ativos"),
    session: Session = Depends(get_session),
    current_user = Depends(verify_user_permission())
) -> List[ProdutoResponse]:
    """
    Lista produtos por faixa de preço.
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a chamada do use case
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    """
    try:
        use_case: ListProdutosUseCase = ListProdutosUseCase()
        request = ListProdutosByPriceRangeRequest(
            min_price=min_price, 
            max_price=max_price, 
            active_only=active_only
        )
        produtos_data = use_case.execute(request.dict(), session)
        return [ProdutoResponse(**produto) for produto in produtos_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos por faixa de preço: {str(e)}")


@produto_router.post(
    "/upload-excel",
    summary="Upload de planilha Excel",
    description="Faz upload de planilha Excel e cria produtos em lote",
    response_model=BulkCreateResponse
)
async def upload_excel_and_create_products(
    file: UploadFile = File(..., description="Arquivo Excel com dados dos produtos"),
    session: Session = Depends(get_session),
    current_user = Depends(verify_user_permission())
) -> BulkCreateResponse:
    """
    Upload de planilha Excel para criação em lote de produtos.
    
    A planilha deve conter as seguintes colunas:
    - codigo: Código único do produto
    - nome: Nome do produto
    - descricao: Descrição do produto (opcional)
    - id_categoria: ID da categoria (deve existir no banco)
    - id_subcategoria: ID da subcategoria (deve existir no banco)
    - valor_base: Valor base do produto (número)
    - ativo: Status ativo (true/false, 1/0, sim/não)
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra o upload e criação
    - Dependency Inversion: Depende de abstrações (use case) não de implementações
    - Open/Closed: Extensível para novos formatos de arquivo sem modificar código existente
    """
    try:
        # Valida tipo de arquivo
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=400,
                detail="Arquivo deve ser do tipo Excel (.xlsx ou .xls)"
            )
        
        # Salva arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Executa criação em lote
            use_case: BulkCreateProdutosUseCase = BulkCreateProdutosUseCase()
            request = {'file_path': temp_file_path}
            result = use_case.execute(request, session)
            
            return BulkCreateResponse(**result)
            
        finally:
            # Remove arquivo temporário
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no upload: {str(e)}")


@produto_router.post(
    "/validate-excel",
    summary="Validar estrutura de planilha Excel",
    description="Valida a estrutura de uma planilha Excel sem processar os dados",
    response_model=ExcelValidationResponse
)
async def validate_excel_structure(
    file: UploadFile = File(..., description="Arquivo Excel para validação"),
    current_user = Depends(verify_user_permission())
) -> ExcelValidationResponse:
    """
    Valida a estrutura de uma planilha Excel.
    
    Verifica se:
    - Arquivo é válido
    - Contém as colunas necessárias
    - Tem dados para processar
    
    Aplica os princípios SOLID:
    - Single Responsibility: Endpoint apenas orquestra a validação
    - Dependency Inversion: Depende de abstrações (service) não de implementações
    """
    try:
        # Valida tipo de arquivo
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=400,
                detail="Arquivo deve ser do tipo Excel (.xlsx ou .xls)"
            )
        
        # Salva arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Valida estrutura
            excel_service: ExcelService = ExcelService()
            validation_result = excel_service.validate_excel_structure(temp_file_path)
            return ExcelValidationResponse(**validation_result)
            
        finally:
            # Remove arquivo temporário
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na validação: {str(e)}")


@produto_router.get(
    "/excel-template",
    summary="Download de template Excel",
    description="Baixa um template Excel com as colunas necessárias para upload de produtos"
)
async def download_excel_template(current_user = Depends(verify_user_permission())):
    """
    Download de template Excel para upload de produtos.
    
    Retorna um arquivo Excel com:
    - Cabeçalhos das colunas necessárias
    - Exemplos de dados
    - Instruções de preenchimento
    """
    try:
        
        # Cria template com colunas necessárias
        template_data = {
            'codigo': ['PROD001', 'PROD002', 'PROD003'],
            'nome': ['Produto Exemplo 1', 'Produto Exemplo 2', 'Produto Exemplo 3'],
            'descricao': ['Descrição do produto 1', 'Descrição do produto 2', 'Descrição do produto 3'],
            'id_categoria': [1, 2, 1],
            'id_subcategoria': [1, 2, 1],
            'valor_base': [10.50, 25.99, 15.75],
            'ativo': [True, True, False]
        }
        
        df = pd.DataFrame(template_data)
        
        # Cria arquivo Excel em memória
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Produtos', index=False)
            
            # Adiciona instruções em outra aba
            instructions = pd.DataFrame({
                'Coluna': ['codigo', 'nome', 'descricao', 'id_categoria', 'id_subcategoria', 'valor_base', 'ativo'],
                'Obrigatório': ['Sim', 'Sim', 'Não', 'Sim', 'Sim', 'Sim', 'Sim'],
                'Tipo': ['Texto', 'Texto', 'Texto', 'Número', 'Número', 'Número', 'Boolean'],
                'Descrição': [
                    'Código único do produto',
                    'Nome do produto',
                    'Descrição detalhada (opcional)',
                    'ID da categoria (deve existir no banco)',
                    'ID da subcategoria (deve existir no banco)',
                    'Valor base do produto',
                    'true/false, 1/0, sim/não'
                ]
            })
            instructions.to_excel(writer, sheet_name='Instruções', index=False)
        
        output.seek(0)
        
        return StreamingResponse(
            io.BytesIO(output.read()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=template_produtos.xlsx"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar template: {str(e)}")
