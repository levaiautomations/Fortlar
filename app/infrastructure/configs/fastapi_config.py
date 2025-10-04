import time
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente antes de qualquer importação de routers
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# Exceptions
from app.application.exceptions.existing_record_exception import ExistingRecordException
from app.application.exceptions.not_found_record_exception import NotFoundRecordException
from app.application.exceptions.forbidden_exception import ForbiddenException
from app.application.exceptions.unprocessable_entity_exception import UnprocessableEntityException

# Routers
from app.presentation.routers.login_router import login_router
from app.presentation.routers.company_router import company_router
from app.presentation.routers.produto_router import produto_router
from app.presentation.routers.categoria_router import categoria_router
from app.presentation.routers.pedido_router import pedido_router
from app.presentation.routers.kit_router import kit_router
from app.presentation.routers.contact_router import contact_router
from app.presentation.routers.address_router import address_router



# ==== Create Web Application Server
application = FastAPI(
    title="Fortlar API",
    description="""
    ## API do Sistema Fortlar
    
    Sistema de gestão de empresas, produtos, pedidos e kits.
    
    ### Funcionalidades Principais:
    - **Empresas**: Gestão completa de empresas com endereços e contatos
    - **Produtos**: Catálogo de produtos com categorias e preços
    - **Pedidos**: Sistema de pedidos com itens e status
    - **Kits**: Gestão de kits de produtos
    - **Categorias**: Organização de produtos por categorias
    
    ### Autenticação:
    - Sistema de login com JWT
    - Diferentes perfis de usuário (ADMIN, CLIENTE)
    
    ### Validações:
    - Validação de CNPJ único
    - Validação de email único
    - Validação de senha forte
    - Validação de dados obrigatórios
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Equipe Fortlar",
        "email": "contato@fortlar.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)
application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ajuste de timezone
os.environ['TZ'] = os.getenv("TZ", "America/Sao_Paulo")
time.tzset()

# Incluir routers
application.include_router(login_router, prefix="/login", tags=["Autenticação"])
application.include_router(login_router, prefix="/password", tags=["Autenticação"])
application.include_router(login_router, prefix="/token", tags=["Autenticação"])
application.include_router(company_router, tags=["Empresas"])
application.include_router(produto_router, tags=["Produtos"])
application.include_router(categoria_router, tags=["Categorias"])
application.include_router(pedido_router, tags=["Pedidos"])
application.include_router(kit_router, tags=["Kits"])
application.include_router(contact_router, tags=["Contatos"])
application.include_router(address_router, tags=["Endereços"])

# ==== Exception handlers ====
@application.exception_handler(ExistingRecordException)
async def existing_record_exception_handler(request: Request, exc: ExistingRecordException):
    return JSONResponse(content={"error": exc.args[0]}, status_code=422)

@application.exception_handler(NotFoundRecordException)
async def not_found_record_exception_handler(request: Request, exc: NotFoundRecordException):
    return JSONResponse(content={"error": exc.args[0]}, status_code=404)

@application.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(content={"error": exc.args[0]}, status_code=403)

@application.exception_handler(UnprocessableEntityException)
async def unprocessable_entity_exception_handler(request: Request, exc: UnprocessableEntityException):
    return JSONResponse(content={"error": exc.args[0]}, status_code=422)

@application.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro não tratado: {exc}")
    return JSONResponse(content={"error": "Erro interno do servidor"}, status_code=500)

