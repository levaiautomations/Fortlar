"""DTOs para responses de produtos"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class ProdutoResponse(BaseModel):
    """Response para produto"""
    id: int
    codigo: str
    nome: str
    descricao: str
    id_categoria: int
    id_subcategoria: int
    valor_base: float
    ativo: bool
    created_at: datetime
    updated_at: datetime
    categoria: Optional[str] = None
    subcategoria: Optional[str] = None


class ListProdutosResponse(BaseModel):
    """Response para lista de produtos"""
    produtos: List[ProdutoResponse]
    total: int
    skip: int
    limit: int
