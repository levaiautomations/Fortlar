"""Implementação do repository para Contact"""

from typing import Optional, List

from app.domain.models.contact_model import Contact
from app.infrastructure.configs.database_config import Session
from app.infrastructure.repositories.contact_repository_interface import IContactRepository
from app.infrastructure.repositories.base_repository import BaseRepository


class ContactRepository(IContactRepository, BaseRepository[Contact]):
    """Repository para operações de Contact com CRUD completo"""

    def __init__(self):
        super().__init__(Contact)

    # Implementação dos métodos abstratos do IContactRepository
    def create(self, contact: Contact, session: Session) -> Contact:
        """Cria um novo contato"""
        return super().create(contact, session)

    def get_by_id(self, contact_id: int, session: Session) -> Optional[Contact]:
        """Busca contato por ID"""
        return super().get_by_id(contact_id, session)

    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[Contact]:
        """Lista todos os contatos"""
        return super().get_all(session, skip, limit)

    def update(self, contact: Contact, session: Session) -> Contact:
        """Atualiza um contato"""
        return super().update(contact, session)

    def delete(self, contact_id: int, session: Session) -> bool:
        """Deleta um contato"""
        return super().delete(contact_id, session)

    def get_by_email(self, email: str, session: Session) -> Optional[Contact]:
        """Busca contato por email"""
        return session.query(Contact).filter(Contact.email == email).first()

    def get_by_company(self, company_id: int, session: Session) -> List[Contact]:
        """Busca contatos por empresa"""
        return session.query(Contact).filter(Contact.id_empresa == company_id).all()

    def exists_by_email(self, email: str, session: Session) -> bool:
        """Verifica se contato existe por email"""
        return session.query(Contact).filter(Contact.email == email).first() is not None

    def get_primary_contact(self, company_id: int, session: Session) -> Optional[Contact]:
        """Busca contato principal da empresa (primeiro contato)"""
        return session.query(Contact).filter(
            Contact.id_empresa == company_id
        ).first()

    def search_by_name(self, name: str, session: Session) -> List[Contact]:
        """Busca contatos por nome"""
        return session.query(Contact).filter(
            Contact.nome.ilike(f"%{name}%")
        ).all()

    def get_by_phone(self, phone: str, session: Session) -> List[Contact]:
        """Busca contatos por telefone ou celular"""
        return session.query(Contact).filter(
            (Contact.telefone == phone) | (Contact.celular == phone)
        ).all()
