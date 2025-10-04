from abc import ABC, abstractmethod
from typing import Optional

from app.domain.models.email_token_modal import EmailToken
from app.domain.models.enumerations.email_token_type_enumerations import EmailTokenTypeEnum
from app.infrastructure.configs.database_config import Session


class IEmailTokenRepository(ABC):


    @abstractmethod
    def exists_by_token_and_company_id_and_type(self, token: str, company_id: int, type: EmailTokenTypeEnum,
                                                session: Session) -> bool:
        pass

    @abstractmethod
    def get_by_company_id(self, company_id: int, session: Session) -> Optional[dict]:
        pass

    @abstractmethod
    def create_email_token(self, email_token: EmailToken, session: Session) -> int:
        pass

    @abstractmethod
    def delete_by_token_and_company_id(self, token: str, company_id: int, session: Session) -> None:
        pass
