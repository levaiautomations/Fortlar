from typing import Optional

from app.domain.models.email_token_modal import EmailToken
from app.domain.models.enumerations.email_token_type_enumerations import EmailTokenTypeEnum
from app.infrastructure.configs.database_config import Session

from sqlalchemy import and_

from app.infrastructure.repositories.email_token_repository_interface import IEmailTokenRepository


class EmailTokenRepository(IEmailTokenRepository):


    def exists_by_token_and_company_id_and_type(self, token: str, company_id: int, type:EmailTokenTypeEnum,
                                                session: Session) -> bool:
        return session.query(EmailToken).filter(and_(EmailToken.token == token,
                                                     EmailToken.id_empresa == company_id,
                                                     EmailToken.tipo == type)
                                                ).first() is not None


    def get_by_company_id(self, company_id: int, session: Session) -> Optional[dict]:
        company = session.query(EmailToken).filter(EmailToken.id_empresa == company_id).first()
        return company.to_dict() if company else None

    def create_email_token(self, email_token: EmailToken, session: Session) -> int:
        session.add(email_token)
        session.flush()
        return email_token.id_empresa

    def delete_by_token_and_company_id(self, token: str, company_id: int, session: Session) -> None:
        session.query(EmailToken).filter(
            and_(EmailToken.token == token, EmailToken.id_empresa == company_id)
        ).delete()
        session.commit()