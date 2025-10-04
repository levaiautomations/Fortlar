"""Container de dependências para injeção de dependência"""

from app.application.service.email_service import EmailService
from app.application.service.hash_service import HashService
from app.application.usecases.impl.create_company_use_case import CreateCompanyUseCase
from app.application.usecases.impl.list_companies_use_case import ListCompaniesUseCase
from app.application.usecases.impl.get_company_use_case import GetCompanyUseCase
from app.application.usecases.impl.update_company_use_case import UpdateCompanyUseCase
from app.application.usecases.impl.delete_company_use_case import DeleteCompanyUseCase
from app.application.usecases.impl.list_produtos_use_case import ListProdutosUseCase

# Repositories
from app.infrastructure.repositories.impl.company_repository_impl import CompanyRepository
from app.infrastructure.repositories.impl.contact_repository_impl import ContactRepository
from app.infrastructure.repositories.impl.address_repository_impl import AddressRepository
from app.infrastructure.repositories.impl.produto_repository_impl import ProdutoRepository
from app.infrastructure.repositories.impl.categoria_repository_impl import CategoriaRepository
from app.infrastructure.repositories.impl.pedido_repository_impl import PedidoRepository
from app.infrastructure.repositories.impl.kit_repository_impl import KitRepository
from app.infrastructure.repositories.impl.email_token_repository_impl import EmailTokenRepository


class DependencyContainer:
    """Container para gerenciar dependências da aplicação"""
    
    def __init__(self):
        # Services
        self._hash_service = HashService()
        self._email_service = EmailService()
        
        # Repositories
        self._company_repository = CompanyRepository()
        self._contact_repository = ContactRepository()
        self._address_repository = AddressRepository()
        self._produto_repository = ProdutoRepository()
        self._categoria_repository = CategoriaRepository()
        self._pedido_repository = PedidoRepository()
        self._kit_repository = KitRepository()
        self._email_token_repository = EmailTokenRepository()
        
        # Use Cases - Company
        self._create_company_use_case = CreateCompanyUseCase(
            company_repository=self._company_repository,
            email_token_repository=self._email_token_repository,
            hash_service=self._hash_service,
            email_service=self._email_service
        )
        
        self._list_companies_use_case = ListCompaniesUseCase(
            company_repository=self._company_repository
        )
        
        self._get_company_use_case = GetCompanyUseCase(
            company_repository=self._company_repository
        )
        
        self._update_company_use_case = UpdateCompanyUseCase(
            company_repository=self._company_repository
        )
        
        self._delete_company_use_case = DeleteCompanyUseCase(
            company_repository=self._company_repository
        )
        
        # Use Cases - Produto
        self._list_produtos_use_case = ListProdutosUseCase(
            produto_repository=self._produto_repository
        )
    
    # Company Use Cases
    @property
    def create_company_use_case(self) -> CreateCompanyUseCase:
        return self._create_company_use_case
    
    @property
    def list_companies_use_case(self) -> ListCompaniesUseCase:
        return self._list_companies_use_case
    
    @property
    def get_company_use_case(self) -> GetCompanyUseCase:
        return self._get_company_use_case
    
    @property
    def update_company_use_case(self) -> UpdateCompanyUseCase:
        return self._update_company_use_case
    
    @property
    def delete_company_use_case(self) -> DeleteCompanyUseCase:
        return self._delete_company_use_case
    
    # Produto Use Cases
    @property
    def list_produtos_use_case(self) -> ListProdutosUseCase:
        return self._list_produtos_use_case
    
    # Services
    @property
    def hash_service(self) -> HashService:
        return self._hash_service
    
    @property
    def email_service(self) -> EmailService:
        return self._email_service
    
    # Repositories
    @property
    def company_repository(self) -> CompanyRepository:
        return self._company_repository
    
    @property
    def contact_repository(self) -> ContactRepository:
        return self._contact_repository
    
    @property
    def address_repository(self) -> AddressRepository:
        return self._address_repository
    
    @property
    def produto_repository(self) -> ProdutoRepository:
        return self._produto_repository
    
    @property
    def categoria_repository(self) -> CategoriaRepository:
        return self._categoria_repository
    
    @property
    def pedido_repository(self) -> PedidoRepository:
        return self._pedido_repository
    
    @property
    def kit_repository(self) -> KitRepository:
        return self._kit_repository


# Instância global do container
container = DependencyContainer()
