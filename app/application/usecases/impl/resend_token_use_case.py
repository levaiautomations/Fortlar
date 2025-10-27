from fastapi import HTTPException, status

from app.application.usecases.use_case import UseCase
from app.domain.models.email_token_modal import EmailToken
from app.domain.models.enumerations.email_token_type_enumerations import EmailTokenTypeEnum
from app.infrastructure.configs.database_config import Session
from app.infrastructure.repositories.company_repository_interface import ICompanyRepository
from app.infrastructure.repositories.email_token_repository_interface import IEmailTokenRepository
from app.infrastructure.repositories.impl.company_repository_impl import CompanyRepositoryImpl
from app.infrastructure.repositories.impl.email_token_repository_impl import EmailTokenRepositoryImpl
from app.application.service.hash_service import HashService
from app.application.service.email_service import EmailService
from app.application.service.email.template.verification_template import verification
from app.presentation.routers.request.resend_token_request import ResendTokenRequest


class ResendTokenUseCase(UseCase[ResendTokenRequest, None]):

    def __init__(self):
        self.company_repo: ICompanyRepository = CompanyRepositoryImpl()
        self.email_token_repo: IEmailTokenRepository = EmailTokenRepositoryImpl()
        self.hash_service: HashService = HashService()
        self.email_service: EmailService = EmailService()

    def execute(self, data: ResendTokenRequest, session: Session = None):
        # Verifica se a empresa existe
        company = self.company_repo.get_by_id(data.company_id, session)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")

        # Busca o email da empresa através do contato
        if not company.contatos or len(company.contatos) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empresa não possui email cadastrado")

        email = company.contatos[0].email

        # Remove tokens antigos de validação de email para esta empresa
        self.email_token_repo.delete_by_company_id_and_type(
            data.company_id, 
            EmailTokenTypeEnum.VALIDACAO_EMAIL, 
            session
        )

        # Gera novo token
        token = self.hash_service.generate_email_token(data.company_id)

        # Cria novo token de email
        email_token = EmailToken(
            id_empresa=data.company_id,
            token=token,
            tipo=EmailTokenTypeEnum.VALIDACAO_EMAIL
        )

        # Gera HTML do email
        html = verification("https://meusite.com/ativar?token=123", token)

        # Envia email
        self.email_service.send_email(email, html, "Reenvio de Token de Validação")

        # Persiste token no banco
        self.email_token_repo.create_email_token(email_token, session)

        return dict(message="Token reenviado com sucesso", company_id=data.company_id)