"""Use case para criação em lote de produtos"""

from typing import List, Dict, Any
from fastapi import HTTPException, status
from decimal import Decimal

from app.application.usecases.use_case import UseCase
from app.application.service.excel_service import ExcelService
from app.domain.models.produto_model import Produto
from app.infrastructure.repositories.produto_repository_interface import IProdutoRepositoryImpl
from app.infrastructure.repositories.categoria_repository_interface import ICategoriaRepositoryImpl
from app.infrastructure.repositories.subcategoria_repository_interface import ISubcategoriaRepositoryImpl
from app.infrastructure.repositories.impl.produto_repository_impl import ProdutoRepositoryImplImpl
from app.infrastructure.repositories.impl.categoria_repository_impl import CategoriaRepositoryImplImpl
from app.infrastructure.repositories.impl.subcategoria_repository_impl import SubcategoriaRepositoryImplImpl


class BulkCreateProdutosUseCase(UseCase[Dict[str, Any], Dict[str, Any]]):
    """Use case para criação em lote de produtos a partir de planilha Excel"""

    def __init__(self):
        self.produto_repository: IProdutoRepositoryImpl = ProdutoRepositoryImplImpl()
        self.categoria_repository: ICategoriaRepositoryImpl = CategoriaRepositoryImplImpl()
        self.subcategoria_repository: ISubcategoriaRepositoryImpl = SubcategoriaRepositoryImplImpl()
        self.excel_service: ExcelService = ExcelService()

    def execute(self, request: Dict[str, Any], session=None) -> Dict[str, Any]:
        """
        Executa o caso de uso de criação em lote de produtos
        
        Args:
            request: Dicionário contendo 'file_path' do arquivo Excel
            session: Sessão do banco de dados
            
        Returns:
            Dicionário com resultado da operação
        """
        try:
            file_path = request.get('file_path')
            if not file_path:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Caminho do arquivo é obrigatório"
                )

            # Processa o arquivo Excel
            produtos_data = self.excel_service.process_excel_file(file_path)
            
            # Valida categorias e subcategorias
            self._validate_categories_and_subcategories(produtos_data, session)
            
            # Processa criação dos produtos
            created_products = []
            errors = []
            
            for index, produto_data in enumerate(produtos_data):
                try:
                    # Verifica se produto já existe
                    existing_produto = self.produto_repository.get_by_codigo(
                        produto_data['codigo'], session
                    )
                    
                    if existing_produto:
                        errors.append({
                            'row': index + 2,  # +2 porque Excel começa em 1 e tem header
                            'codigo': produto_data['codigo'],
                            'error': 'Produto com este código já existe'
                        })
                        continue
                    
                    # Cria entidade Produto
                    produto = self._create_produto_entity(produto_data)
                    
                    # Persiste no banco
                    created_produto = self.produto_repository.create(produto, session)
                    created_products.append(self._build_produto_response(created_produto))
                    
                except Exception as e:
                    errors.append({
                        'row': index + 2,
                        'codigo': produto_data.get('codigo', 'N/A'),
                        'error': str(e)
                    })
                    continue
            
            # Commit da transação
            session.commit()
            
            return {
                'success': True,
                'total_processed': len(produtos_data),
                'created_count': len(created_products),
                'error_count': len(errors),
                'created_products': created_products,
                'errors': errors,
                'message': f"Processados {len(produtos_data)} produtos. "
                          f"Criados: {len(created_products)}, "
                          f"Erros: {len(errors)}"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar produtos em lote: {str(e)}"
            )

    def _validate_categories_and_subcategories(
        self, 
        produtos_data: List[Dict[str, Any]], 
        session
    ) -> None:
        """
        Valida se todas as categorias e subcategorias existem no banco
        
        Args:
            produtos_data: Lista de dados dos produtos
            session: Sessão do banco de dados
            
        Raises:
            HTTPException: Se categoria ou subcategoria não existir
        """
        # Coleta IDs únicos
        categoria_ids = set()
        subcategoria_ids = set()
        
        for produto_data in produtos_data:
            categoria_ids.add(produto_data['id_categoria'])
            subcategoria_ids.add(produto_data['id_subcategoria'])
        
        # Valida categorias
        for categoria_id in categoria_ids:
            categoria = self.categoria_repository.get_by_id(categoria_id, session)
            if not categoria:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Categoria com ID {categoria_id} não encontrada"
                )
        
        # Valida subcategorias
        for subcategoria_id in subcategoria_ids:
            subcategoria = self.subcategoria_repository.get_by_id(subcategoria_id, session)
            if not subcategoria:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Subcategoria com ID {subcategoria_id} não encontrada"
                )

    def _create_produto_entity(self, produto_data: Dict[str, Any]) -> Produto:
        """
        Cria entidade Produto a partir dos dados processados
        
        Args:
            produto_data: Dados do produto processados
            
        Returns:
            Entidade Produto criada
        """
        return Produto(
            codigo=produto_data['codigo'],
            nome=produto_data['nome'],
            descricao=produto_data['descricao'],
            id_categoria=produto_data['id_categoria'],
            id_subcategoria=produto_data['id_subcategoria'],
            valor_base=produto_data['valor_base'],
            ativo=produto_data['ativo']
        )

    def _build_produto_response(self, produto: Produto) -> Dict[str, Any]:
        """
        Constrói resposta do produto criado
        
        Args:
            produto: Entidade Produto
            
        Returns:
            Dicionário com dados do produto para resposta
        """
        return {
            'id': produto.id_produto,
            'codigo': produto.codigo,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'id_categoria': produto.id_categoria,
            'id_subcategoria': produto.id_subcategoria,
            'valor_base': float(produto.valor_base),
            'ativo': produto.ativo,
            'created_at': produto.created_at.isoformat(),
            'updated_at': produto.updated_at.isoformat()
        }
