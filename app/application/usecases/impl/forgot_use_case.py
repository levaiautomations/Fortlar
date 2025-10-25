import uuid
from fastapi import HTTPException, status

from app.application.service.email.template.reset_password_template import reset_password
from app.application.service.email_service import EmailService
from app.application.service.hash_service import HashService
from app.application.usecases.use_case import UseCase
from app.domain.models.enumerations.email_token_type_enumerations import EmailTokenTypeEnum
from app.infrastructure.repositories.company_repository_interface import ICompanyRepository
from app.infrastructure.repositories.email_token_repository_interface import IEmailTokenRepository
from app.infrastructure.repositories.impl.company_repository_impl import CompanyRepositoryImpl
from app.infrastructure.repositories.impl.email_token_repository_impl import EmailTokenRepositoryImpl
from app.presentation.routers.request.forgot_password_request import ForgotPasswordRequest
from app.domain.models.email_token_modal import EmailToken
from app.infrastructure.configs.database_config import Session

class ForgotPasswordUseCase(UseCase[ForgotPasswordRequest, None]):

    def __init__(self):
        self.company_repo: ICompanyRepository = CompanyRepositoryImpl()
        self.email_token_repo: IEmailTokenRepository = EmailTokenRepositoryImpl()
        self.hash_service: HashService = HashService()
        self.email_service: EmailService = EmailService()

    def execute(self, data: ForgotPasswordRequest, session: Session = None) -> None:
        company = self.company_repo.find_by_email_or_cnpj(data.email.__str__(), session)

        if not company:
            return

        # Gera token de reset
        token = self.hash_service.generate_email_token(company.id_empresa)

        # salva no banco
        email_token = EmailToken(
            id_empresa=company.id_empresa,
            token=token,
            tipo=EmailTokenTypeEnum.RESET_SENHA
        )
        self.email_token_repo.create_email_token(email_token, session)
        session.commit()

        # TODO: enviar e-mail real
        print(f"Enviar link para reset: https://suaapp.com/reset-password?token={token}&company_id={company.id_empresa}")


    def send_email(self, company_id: int, email: str, session):
        # Token de verificação
        token = self.hash_service.generate_email_token(company_id)

        email_token = EmailToken(id_empresa=company_id, token=token, tipo=EmailTokenTypeEnum.RESET_SENHA)

        html = reset_password("https://meusite.com/ativar?token=123", token)

        # Envio de e-mail
        self.email_service.send_email(email, html,"Redefinição de Senha")

        self.email_token_repo.create_email_token(email_token, session)
