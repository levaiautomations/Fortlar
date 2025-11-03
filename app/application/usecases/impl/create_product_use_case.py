"""Use case para upload completo de planilha CSV ou Excel com kits, regiões, prazos e produtos"""

from typing import Dict, Any, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.application.usecases.use_case import UseCase
from app.application.service.excel_loader_service import ExcelLoaderService
from app.infrastructure.repositories.product_repository_interface import IProductRepository
from app.infrastructure.repositories.category_repository_interface import ICategoryRepository
from app.infrastructure.repositories.subcategory_repository_interface import ISubcategoryRepository
from app.infrastructure.repositories.product_image_repository_interface import IProductImageRepository
from app.infrastructure.repositories.impl.product_repository_impl import ProductRepositoryImpl
from app.infrastructure.repositories.impl.category_repository_impl import CategoryRepositoryImpl
from app.infrastructure.repositories.impl.subcategory_repository_impl import SubcategoryRepositoryImpl
from app.infrastructure.repositories.impl.product_image_repository_impl import ProductImageRepositoryImpl

from app.domain.models.product_model import Product
from app.domain.models.product_image_model import ProductImage

logger = logging.getLogger(__name__)


class CreateProductUseCase(UseCase[Dict[str, Any], Dict[str, Any]]):
    """Use case para upload completo de planilha CSV ou Excel"""
    
    def __init__(self):
        self.loader = ExcelLoaderService()
        self.product_repository: IProductRepository = ProductRepositoryImpl()
        self.category_repository: ICategoryRepository = CategoryRepositoryImpl()
        self.subcategory_repository: ISubcategoryRepository = SubcategoryRepositoryImpl()
        self.product_image_repository: IProductImageRepository = ProductImageRepositoryImpl()

    def execute(self, request: Dict[str, Any], session: Session = None) -> Dict[str, Any]:
        """
        Executa o upload completo da planilha
        
        Args:
            request: Dicionário contendo 'file_path' e 'file_format' ('csv' ou 'excel')
            session: Sessão do banco de dados
            
        Returns:
            Dicionário com resumo da operação
        """

        file_path = request.get('file_path')
        if not file_path:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Caminho do arquivo é obrigatório"
            )

        file_format = request.get('file_format', 'auto')
        self.loader.file_format = file_format

        summary = {
            "categorias_created": 0,
            "subcategorias_created": 0,
            "produtos_created": 0,
            "produtos_updated": 0,
            "imagens_created": 0,
            "errors": []
        }

        try:
            # Lê e valida a planilha
            df = self.loader.read(file_path)
            
            # Detecta formato pelas colunas (CSV e Excel novo têm mesma estrutura)
            has_csv_cols = all(col in df.columns for col in ['codigo', 'Nome'])
            has_old_excel_cols = all(col in df.columns for col in ['PRODUTO', 'CATEGORIA'])
            
            # Se tiver colunas do novo formato (CSV), usa processamento CSV mesmo que seja Excel
            if has_csv_cols:
                detected_format = 'csv'
            elif has_old_excel_cols:
                detected_format = 'excel'
            else:
                # Default para CSV se não conseguir detectar
                detected_format = 'csv'
                logger.warning(f"Formato não identificado claramente, usando processamento CSV. Colunas: {list(df.columns)}")
            
            self.loader.validate_columns(df, detected_format)
            
            # Extrai dados (kits_map não é mais necessário, kits são campos do Product)
            produtos_data, _ = self.loader.extract_entities(df, detected_format)
            
            if not produtos_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Nenhum produto válido encontrado na planilha"
                )

            # Dicionários para evitar duplicatas no mesmo run
            seen_categorias = {}
            seen_subcategorias = {}
            seen_produtos = {}  # Para CSV: mapeia código -> produto

            # Inicia transação
            try:
                if detected_format == 'csv':
                    self._process_csv_format(
                        produtos_data, session, summary,
                        seen_categorias, seen_subcategorias, seen_produtos
                    )
                else:
                    self._process_excel_format(
                        produtos_data, session, summary,
                        seen_categorias, seen_subcategorias
                    )

            except Exception as e:
                session.rollback()
                logger.exception("Erro no processamento, rollback realizado")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erro no processamento: {str(e)}"
                )

        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Erro no upload em massa")
            if session:
                session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao processar planilha: {str(e)}"
            )

        return {
            "success": True,
            "message": "Upload realizado com sucesso",
            "summary": summary
        }

    def _process_csv_format(
        self, produtos_data, session, summary,
        seen_categorias, seen_subcategorias, seen_produtos
    ):
        """Processa formato CSV"""
        for idx, p in enumerate(produtos_data):
            try:
                # Busca categoria por ID
                categoria = None
                id_categoria = p.get('id_categoria')
                if id_categoria:
                    if id_categoria not in seen_categorias:
                        categoria = self.category_repository.get_by_id(id_categoria, session)
                        if not categoria:
                            summary["errors"].append({
                                "row": idx + 2,
                                "type": "produto",
                                "codigo": p.get('codigo', 'N/A'),
                                "error": f"Categoria com ID {id_categoria} não encontrada"
                            })
                            continue
                        seen_categorias[id_categoria] = categoria
                    else:
                        categoria = seen_categorias[id_categoria]
                else:
                    summary["errors"].append({
                        "row": idx + 2,
                        "type": "produto",
                        "codigo": p.get('codigo', 'N/A'),
                        "error": "ID da categoria não informado"
                    })
                    continue

                # Busca subcategoria por ID (opcional)
                sub = None
                id_subcategoria = p.get('id_subcategoria')
                if id_subcategoria:
                    sub_key = f"{id_categoria}::{id_subcategoria}"
                    if sub_key not in seen_subcategorias:
                        sub = self.subcategory_repository.get_by_id(id_subcategoria, session)
                        if not sub or sub.id_categoria != id_categoria:
                            summary["errors"].append({
                                "row": idx + 2,
                                "type": "produto",
                                "codigo": p.get('codigo', 'N/A'),
                                "error": f"Subcategoria com ID {id_subcategoria} não encontrada ou não pertence à categoria {id_categoria}"
                            })
                            continue
                        seen_subcategorias[sub_key] = sub
                    else:
                        sub = seen_subcategorias[sub_key]

                # Busca ou cria produto por código
                codigo = p.get('codigo', '').strip()
                nome = p.get('nome', '').strip()
                if not codigo and not nome:
                    continue

                existing_product = None
                if codigo:
                    existing_product = self.product_repository.get_by_codigo(codigo, session)
                    seen_produtos[codigo] = existing_product

                if existing_product:
                    # Atualiza produto existente
                    updated = False
                    if p.get('descricao') and existing_product.descricao != p.get('descricao'):
                        existing_product.descricao = p.get('descricao')
                        updated = True
                    if p.get('valor_base') is not None and existing_product.valor_base != p.get('valor_base'):
                        existing_product.valor_base = p.get('valor_base')
                        updated = True
                    if categoria and existing_product.id_categoria != categoria.id_categoria:
                        existing_product.id_categoria = categoria.id_categoria
                        updated = True
                    if sub and existing_product.id_subcategoria != sub.id_subcategoria:
                        existing_product.id_subcategoria = sub.id_subcategoria
                        updated = True
                    
                    # Atualiza quantidade e cod_kit
                    quantidade = p.get('quantidade', 1)
                    if existing_product.quantidade != quantidade:
                        existing_product.quantidade = quantidade
                        updated = True
                    
                    codigo_amarracao = p.get('codigo_amarracao')
                    # cod_kit agora é string (mesmo tipo do codigo)
                    cod_kit = codigo_amarracao if codigo_amarracao else None
                    logger.debug(f"Produto {codigo}: codigo_amarracao={codigo_amarracao} -> cod_kit={cod_kit}")
                    
                    # Compara considerando None
                    current_cod_kit = existing_product.cod_kit if existing_product.cod_kit is not None else None
                    new_cod_kit = cod_kit if cod_kit is not None else None
                    
                    if current_cod_kit != new_cod_kit:
                        existing_product.cod_kit = cod_kit
                        updated = True
                        logger.debug(f"Atualizando cod_kit do produto {codigo}: {current_cod_kit} -> {new_cod_kit}")
                    
                    if updated:
                        self.product_repository.update(existing_product, session)
                        summary["produtos_updated"] += 1
                    produto = existing_product
                    
                    # Processa imagens do produto (atualiza/remove/adiciona)
                    self._process_product_images(produto, p.get('image_urls', []), session, summary)
                else:
                    # Cria novo produto
                    if not codigo:
                        codigo = f"PROD-{nome[:20].upper().replace(' ', '-')}"
                        counter = 1
                        original_codigo = codigo
                        while self.product_repository.get_by_codigo(codigo, session):
                            codigo = f"{original_codigo}-{counter}"
                            counter += 1
                    
                    # cod_kit agora é string (mesmo tipo do codigo)
                    codigo_amarracao = p.get('codigo_amarracao')
                    cod_kit = codigo_amarracao if codigo_amarracao else None
                    logger.debug(f"Criando produto {codigo}: codigo_amarracao={codigo_amarracao} -> cod_kit={cod_kit}")
                    
                    # Obtém quantidade
                    quantidade = p.get('quantidade', 1)
                    
                    produto = Product(
                        codigo=codigo,
                        nome=nome,
                        descricao=p.get('descricao'),
                        id_categoria=categoria.id_categoria if categoria else None,
                        id_subcategoria=sub.id_subcategoria if sub else None,
                        valor_base=p.get('valor_base') or 0,
                        quantidade=quantidade,
                        cod_kit=cod_kit,
                        ativo=True
                    )
                    produto = self.product_repository.create(produto, session)
                    seen_produtos[codigo] = produto
                    summary["produtos_created"] += 1
                    
                    # Processa imagens do produto
                    self._process_product_images(produto, p.get('image_urls', []), session, summary)

            except Exception as e:
                summary["errors"].append({
                    "row": idx + 2,
                    "type": "produto",
                    "codigo": p.get('codigo', 'N/A'),
                    "error": str(e)
                })
                logger.warning(f"Erro ao processar linha {idx+2}: {e}")

    def _process_product_images(self, produto: Product, image_urls: List[str], session: Session, summary: Dict[str, Any]):
        """
        Processa as imagens do produto, criando registros ProductImage.
        Cada URL do array cria um objeto novo na tabela imagens_produto.
        """
        if not image_urls:
            logger.debug(f"Produto {produto.codigo} sem imagens para processar")
            return
        
        try:
            logger.info(f"Processando {len(image_urls)} URL(s) de imagem para o produto {produto.codigo}")
            
            # Busca imagens existentes do produto usando o repository
            existing_images = self.product_image_repository.get_by_produto(produto.id_produto, session)
            
            existing_urls = {img.url for img in existing_images}
            # Remove duplicatas mantendo a ordem (para logs consistentes)
            unique_urls = list(dict.fromkeys(image_urls))
            
            logger.debug(f"Produto {produto.codigo}: {len(existing_images)} imagem(ns) existente(s), {len(unique_urls)} URL(s) para processar")
            
            # Remove imagens que não estão mais na lista usando o repository
            for img in existing_images:
                if img.url not in unique_urls:
                    self.product_image_repository.delete(img.id_imagem, session)
                    logger.debug(f"Removendo imagem ID {img.id_imagem} (URL: '{img.url[:80]}...') do produto {produto.codigo}")
            
            # Adiciona novas imagens - CADA URL cria um objeto novo na tabela imagens_produto usando o repository
            created_count = 0
            for idx, url in enumerate(unique_urls, start=1):
                url_clean = url.strip()
                
                # Valida URL básica
                if not url_clean:
                    logger.warning(f"URL vazia ignorada na posição {idx} para produto {produto.codigo}")
                    continue
                
                if not (url_clean.startswith('http://') or url_clean.startswith('https://') or url_clean.startswith('/')):
                    logger.warning(f"URL de imagem inválida para produto {produto.codigo} (posição {idx}): {url_clean[:80]}...")
                    continue
                
                # Verifica se já existe (usa o set em memória para performance)
                if url_clean in existing_urls:
                    logger.debug(f"URL já existe para produto {produto.codigo}, ignorando: {url_clean[:80]}...")
                    continue
                
                # Cria um NOVO objeto ProductImage para esta URL usando o repository
                product_image = ProductImage(
                    id_produto=produto.id_produto,
                    url=url_clean
                )
                created_image = self.product_image_repository.create(product_image, session)
                created_count += 1
                summary["imagens_created"] += 1
                
                logger.info(f"Criado registro ProductImage ID {created_image.id_imagem} para produto {produto.codigo} - URL {idx}/{len(unique_urls)}: {url_clean[:80]}...")
            
            logger.info(f"Produto {produto.codigo}: {created_count} nova(s) imagem(ns) criada(s) em imagens_produto")
                        
        except Exception as e:
            logger.error(f"Erro ao processar imagens do produto {produto.codigo}: {e}", exc_info=True)
            summary["errors"].append({
                "type": "imagem",
                "product_codigo": produto.codigo,
                "error": str(e)
            })

    def _process_excel_format(
        self, produtos_data, session, summary,
        seen_categorias, seen_subcategorias
    ):
        """Processa formato Excel (método original) - TODO: Implementar se necessário"""
        # Processa produtos
        for idx, p in enumerate(produtos_data):
            try:
                # Category
                categoria = None
                cat_key = p.get('categoria', '').strip()
                if not cat_key:
                    summary["errors"].append({
                        "row": idx + 2,
                        "type": "produto",
                        "nome": p.get('nome', 'N/A'),
                        "error": "Category não informada"
                    })
                    continue
                
                if cat_key:
                    if cat_key not in seen_categorias:
                        # Tenta buscar existente
                        categoria = self.category_repository.get_by_name(cat_key, session)
                        if not categoria:
                            # Cria nova
                            from app.domain.models.category_model import Category
                            categoria = Category(nome=cat_key)
                            categoria = self.category_repository.create(categoria, session)
                            summary["categorias_created"] += 1
                        seen_categorias[cat_key] = categoria
                    else:
                        categoria = seen_categorias[cat_key]

                # Subcategory
                sub = None
                sub_key = p.get('subcategoria', '').strip()
                if sub_key and categoria:
                    sc_key = f"{cat_key}::{sub_key}"
                    if sc_key not in seen_subcategorias:
                        # Busca existente (por nome e categoria)
                        sub = self.subcategory_repository.get_by_name(sub_key, session)
                        if sub and sub.id_categoria != categoria.id_categoria:
                            # Nome existe mas para outra categoria, cria novo
                            sub = None
                        if not sub:
                            # Cria nova
                            from app.domain.models.subcategory_model import Subcategory
                            sub = Subcategory(nome=sub_key, id_categoria=categoria.id_categoria)
                            sub = self.subcategory_repository.create(sub, session)
                            summary["subcategorias_created"] += 1
                        seen_subcategorias[sc_key] = sub
                    else:
                        sub = seen_subcategorias[sc_key]

                # Product - busca por nome exato
                product_nome = p.get('nome', '').strip()
                product_code = p.get('codigo', '').strip()
                if not product_code:
                    continue
                    
                existing_product = self.product_repository.get_by_codigo(product_code, session)
                
                if existing_product:
                    # Atualiza produto existente
                    updated = False
                    if p.get('descricao') and existing_product.descricao != p.get('descricao'):
                        existing_product.descricao = p.get('descricao')
                        updated = True
                    if p.get('valor_base') is not None and existing_product.valor_base != p.get('valor_base'):
                        existing_product.valor_base = p.get('valor_base')
                        updated = True
                    if categoria and existing_product.id_categoria != categoria.id_categoria:
                        existing_product.id_categoria = categoria.id_categoria
                        updated = True
                    if sub and existing_product.id_subcategoria != sub.id_subcategoria:
                        existing_product.id_subcategoria = sub.id_subcategoria
                        updated = True
                    if updated:
                        self.product_repository.update(existing_product, session)
                        summary["produtos_updated"] += 1
                else:
                    produto = Product(
                        codigo=product_code,
                        nome=product_nome,
                        descricao=p.get('descricao'),
                        id_categoria=categoria.id_categoria if categoria else None,
                        id_subcategoria=sub.id_subcategoria if sub else None,
                        valor_base=p.get('valor_base') or 0,
                        quantidade=1,  # Excel antigo não tem quantidade
                        cod_kit=None,  # Excel antigo não tem código amarração
                        ativo=True
                    )
                    self.product_repository.create(produto, session)
                    summary["produtos_created"] += 1

            except Exception as e:
                summary["errors"].append({
                    "row": idx + 2,
                    "type": "produto",
                    "nome": p.get('nome', 'N/A'),
                    "error": str(e)
                })
