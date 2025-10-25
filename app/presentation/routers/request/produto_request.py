"""DTOs para requests de produtos"""

from typing import Optional
from pydantic import BaseModel, Field


class ListProdutosRequest(BaseModel):
    """Request para listar produtos"""
    skip: int = Field(0, ge=0, description="Número de registros para pular")
    limit: int = Field(100, ge=1, le=1000, description="Número máximo de registros")
    active_only: bool = Field(True, description="Filtrar apenas produtos ativos")
    categoria_id: Optional[int] = Field(None, description="Filtrar por categoria")
    subcategoria_id: Optional[int] = Field(None, description="Filtrar por subcategoria")
    search_name: Optional[str] = Field(None, description="Buscar por nome")
    min_price: Optional[float] = Field(None, ge=0, description="Preço mínimo")
    max_price: Optional[float] = Field(None, ge=0, description="Preço máximo")


class ListProdutosByCategoriaRequest(BaseModel):
    """Request para listar produtos por categoria"""
    categoria_id: int = Field(..., description="ID da categoria")
    active_only: bool = Field(True, description="Filtrar apenas produtos ativos")


class ListProdutosBySubcategoriaRequest(BaseModel):
    """Request para listar produtos por subcategoria"""
    subcategoria_id: int = Field(..., description="ID da subcategoria")
    active_only: bool = Field(True, description="Filtrar apenas produtos ativos")


class SearchProdutosRequest(BaseModel):
    """Request para buscar produtos"""
    q: str = Field(..., description="Termo de busca")
    active_only: bool = Field(True, description="Filtrar apenas produtos ativos")


class ListProdutosByPriceRangeRequest(BaseModel):
    """Request para listar produtos por faixa de preço"""
    min_price: float = Field(..., ge=0, description="Preço mínimo")
    max_price: float = Field(..., ge=0, description="Preço máximo")
    active_only: bool = Field(True, description="Filtrar apenas produtos ativos")
