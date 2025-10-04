from typing import Optional
from fastapi import HTTPException, status

from app.application.service.email.template.verification_template import verification
from app.application.service.email_service import EmailService
from app.application.service.hash_service import HashService
from app.application.usecases.use_case import UseCase
from app.domain.models.address_model import Address
from app.domain.models.contact_model import Contact
from app.domain.models.email_token_modal import EmailToken
from app.domain.models.enumerations.email_token_type_enumerations import EmailTokenTypeEnum
from app.domain.models.enumerations.role_enumerations import RoleEnum
from app.domain.services.company_domain_service import CompanyDomainService
from app.domain.exceptions.company_exceptions import CompanyAlreadyExistsException
from app.infrastructure.repositories.company_repository_interface import ICompanyRepository
from app.infrastructure.repositories.email_token_repository_interface import IEmailTokenRepository
from app.infrastructure.utils.validate_password import validate_password
from app.presentation.routers.request.company_request import CompanyRequest
from app.presentation.routers.response.company_response import CompanyResponse


class CreateCompanyUseCase(UseCase[CompanyRequest, CompanyResponse]):
    """Use case para criação de empresas"""

    def __init__(
        self,
        company_repository: ICompanyRepository,
        email_token_repository: IEmailTokenRepository,
        hash_service: HashService,
        email_service: EmailService
    ):
        self.company_repo = company_repository
        self.email_token_repo = email_token_repository
        self.hash_service = hash_service
        self.email_service = email_service


    def execute(self, request: CompanyRequest, session=None) -> CompanyResponse:
        """Executa o caso de uso de criação de empresa"""
        self._validate_request(request, session)
        
        # Cria a empresa usando o service de domínio
        company = self._create_company_entity(request)
        
        # Cria endereço e contato
        address = self._create_address_entity(request)
        contact = self._create_contact_entity(request)
        
        # Associa endereço e contato à empresa
        company.enderecos.append(address)
        company.contatos.append(contact)

        # Persiste no banco
        company_id = self.company_repo.create_company_with_address_and_contact(company, session)

        # Envia email de verificação
        self._send_verification_email(company_id, request.contato.email, session)

        # Retorna resposta
        company = self.company_repo.get_by_id(company_id, session=session)
        return self._build_company_response(company)
    
    def _build_company_response(self, company) -> CompanyResponse:
        """Constrói a resposta da empresa com endereços e contatos"""
        from app.presentation.routers.response.company_response import AddressResponse, ContactResponse
        
        # Converte endereços
        address_responses = [
            AddressResponse(
                id_endereco=addr.id_endereco,
                cep=addr.cep,
                numero=addr.numero,
                complemento=addr.complemento,
                bairro=addr.bairro,
                cidade=addr.cidade,
                uf=addr.uf,
                ibge=addr.ibge
            ) for addr in company.enderecos
        ]
        
        # Converte contatos
        contact_responses = [
            ContactResponse(
                id_contato=contact.id_contato,
                nome=contact.nome,
                telefone=contact.telefone,
                celular=contact.celular,
                email=contact.email
            ) for contact in company.contatos
        ]
        
        return CompanyResponse(
            id_empresa=company.id_empresa,
            cnpj=company.cnpj,
            razao_social=company.razao_social,
            nome_fantasia=company.nome_fantasia,
            perfil=company.perfil.value,
            ativo=company.ativo,
            created_at=company.created_at,
            updated_at=company.updated_at,
            enderecos=address_responses,
            contatos=contact_responses
        )
    
    def _validate_request(self, request: CompanyRequest, session) -> None:
        """Valida os dados da requisição"""
        if self.company_repo.exists_by_cnpj(request.cnpj, session=session):
            raise CompanyAlreadyExistsException("CNPJ já cadastrado")
        
        if self.company_repo.exists_by_email(request.contato.email, session=session):
            raise CompanyAlreadyExistsException("Email já cadastrado")
        
        if not validate_password(request.senha):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha inválida. Deve ter no mínimo 8 caracteres, uma letra maiúscula, um número e um caractere especial."
            )
    
    def _create_company_entity(self, request: CompanyRequest):
        """Cria a entidade Company usando o service de domínio"""
        password_hash = self.hash_service.hash_password(request.senha)
        
        return CompanyDomainService.create_company(
            cnpj=request.cnpj,
            razao_social=request.razao_social,
            nome_fantasia=request.nome_fantasia,
            senha_hash=password_hash,
            id_vendedor=1,  # TODO: Obter do contexto de autenticação
            perfil=RoleEnum.CLIENTE,
            ativo=False
        )
    
    def _create_address_entity(self, request: CompanyRequest) -> Address:
        """Cria a entidade Address"""
        return Address(
            id_endereco=None,
            cep=request.endereco.cep,
            numero=request.endereco.numero,
            complemento=request.endereco.complemento,
            bairro=request.endereco.bairro,
            cidade=request.endereco.cidade,
            uf=request.endereco.uf,
            ibge=request.endereco.ibge,
        )
    
    def _create_contact_entity(self, request: CompanyRequest) -> Contact:
        """Cria a entidade Contact"""
        return Contact(
            id_contato=None,
            nome=request.contato.nome,
            telefone=request.contato.telefone,
            celular=request.contato.celular,
            email=request.contato.email,
        )


    def _send_verification_email(self, company_id: int, email: str, session) -> None:
        """Envia email de verificação para a empresa"""
        token = self.hash_service.generate_email_token(company_id)
        
        # Cria token de email
        email_token = EmailToken(
            id_email=None, 
            id_empresa=company_id, 
            token=token, 
            tipo=EmailTokenTypeEnum.VALIDACAO_EMAIL
        )
        
        # Gera HTML do email
        html = verification("https://meusite.com/ativar?token=123", token)
        
        # Envia email
        self.email_service.send_email(email, html, "Primeiro Acesso")
        
        # Persiste token
        self.email_token_repo.create_email_token(email_token, session)







