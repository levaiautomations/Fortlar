"""Router para operações de Categorias"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from typing import List, Optional
from loguru import logger

# Repositories
from app.infrastructure.repositories.impl.category_repository_impl import CategoryRepositoryImpl

# Use Cases
from app.application.usecases.impl.create_category_use_case import CreateCategoryUseCase

# Request/Response Models
from app.presentation.routers.request.category_request import CategoryRequest
from app.presentation.routers.response.category_response import CategoryResponse

# Configs
from app.infrastructure.configs.database_config import Session
from app.infrastructure.configs.session_config import get_session
from app.infrastructure.configs.security_config import verify_user_permission
from app.domain.models.enumerations.role_enumerations import RoleEnum

category_router = APIRouter(
    prefix="/category",
    tags=["Categorias"],
    responses={
        404: {"description": "Category não encontrada"},
        422: {"description": "Dados inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)


# Dependency Injection Functions removidas - usando padrão simples


@category_router.post(
    "/",
    response_model=CategoryResponse,
    status_code=201,
    summary="Create category",
    description="Creates a new category with subcategories"
)
async def create_category(
    category: CategoryRequest,
    session: Session = Depends(get_session),
    current_user = Depends(verify_user_permission(role=RoleEnum.ADMIN))
) -> CategoryResponse:
    """Creates a new category with subcategories"""
    try:
        logger.info('=== Creating category ===')
        use_case: CreateCategoryUseCase = CreateCategoryUseCase()
        return use_case.execute(category, session=session)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating category: {str(e)}")


@category_router.get(
    "/",
    summary="Listar categorias",
    description="Lista todas as categorias"
)
async def list_categorias(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    search_name: Optional[str] = Query(None, description="Buscar por nome"),
    with_products: bool = Query(False, description="Incluir apenas categorias com produtos"),
    session: Session = Depends(get_session)
) -> List[dict]:
    """Lista categorias com filtros opcionais"""
    try:
        categoria_repo: CategoryRepositoryImpl = CategoryRepositoryImpl()
        
        if search_name:
            categorias = categoria_repo.search_by_name(search_name, session)
        elif with_products:
            categorias = categoria_repo.get_categories_with_products(session)
        else:
            categorias = categoria_repo.get_all(session, skip, limit)
        
        # Debug: verificar se categorias é None
        if categorias is None:
            categorias = []
        
        return [
            {
                "id_categoria": cat.id_categoria,
                "nome": cat.nome,
                "created_at": cat.created_at.isoformat(),
                "updated_at": cat.updated_at.isoformat()
            }
            for cat in categorias
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar categorias: {str(e)}")


@category_router.get(
    "/{categoria_id}",
    summary="Buscar categoria por ID",
    description="Busca uma categoria específica pelo ID"
)
async def get_categoria(
    categoria_id: int = Path(..., description="ID da categoria"),
    session: Session = Depends(get_session)
) -> dict:
    """Busca categoria por ID"""
    try:
        categoria_repo: CategoryRepositoryImpl = CategoryRepositoryImpl()
        categoria = categoria_repo.get_by_id(categoria_id, session)
        
        if not categoria:
            raise HTTPException(status_code=404, detail="Category não encontrada")
        
        return {
            "id": categoria.id,
            "nome": categoria.nome,
            "created_at": categoria.created_at.isoformat(),
            "updated_at": categoria.updated_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar categoria: {str(e)}")


@category_router.get(
    "/{categoria_id}/produtos",
    summary="Listar produtos da categoria",
    description="Lista todos os produtos de uma categoria específica"
)
async def list_produtos_by_categoria(
    categoria_id: int = Path(..., description="ID da categoria"),
    active_only: bool = Query(True, description="Filtrar apenas produtos ativos"),
    session: Session = Depends(get_session)
) -> List[dict]:
    """Lista produtos de uma categoria"""
    try:
        from app.infrastructure.repositories.impl.product_repository_impl import ProductRepositoryImpl
        produto_repo: ProductRepositoryImpl = ProductRepositoryImpl()
        
        if active_only:
            produtos = produto_repo.get_active_products(session)
            produtos = [p for p in produtos if p.id_categoria == categoria_id]
        else:
            produtos = produto_repo.get_by_categoria(categoria_id, session)
        
        return [
            {
                "id": prod.id,
                "codigo": prod.codigo,
                "nome": prod.nome,
                "descricao": prod.descricao,
                "valor_base": float(prod.valor_base),
                "ativo": prod.ativo,
                "created_at": prod.created_at.isoformat(),
                "updated_at": prod.updated_at.isoformat()
            }
            for prod in produtos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos da categoria: {str(e)}")


@category_router.get(
    "/{categoria_id}/subcategorias",
    summary="Listar subcategorias da categoria",
    description="Lista todas as subcategorias de uma categoria específica"
)
async def list_subcategorias_by_categoria(
    categoria_id: int = Path(..., description="ID da categoria"),
    session: Session = Depends(get_session)
) -> List[dict]:
    """Lista subcategorias de uma categoria"""
    try:
        categoria_repo: CategoryRepositoryImpl = CategoryRepositoryImpl()
        categoria = categoria_repo.get_by_id(categoria_id, session)
        
        if not categoria:
            raise HTTPException(status_code=404, detail="Category não encontrada")
        
        return [
            {
                "id": sub.id,
                "nome": sub.nome,
                "id_categoria": sub.id_categoria,
                "created_at": sub.created_at.isoformat(),
                "updated_at": sub.updated_at.isoformat()
            }
            for sub in categoria.subcategorias
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar subcategorias: {str(e)}")
