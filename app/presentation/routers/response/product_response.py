"""DTOs para responses de produtos"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class ProductResponse(BaseModel):
    """Response para produto"""
    id_produto: int
    codigo: str
    nome: str
    descricao: Optional[str] = None
    quantidade: int = 1
    cod_kit: Optional[str] = None
    id_categoria: int
    id_subcategoria: Optional[int] = None
    valor_base: float
    ativo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    categoria: Optional[str] = None
    subcategoria: Optional[str] = None
    imagens: List[str] = []


