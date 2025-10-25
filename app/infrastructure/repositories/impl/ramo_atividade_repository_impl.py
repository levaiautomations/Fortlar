from typing import Optional, List

from app.domain.models.ramo_atividade_model import RamoAtividade
from app.infrastructure.configs.database_config import Session
from app.infrastructure.repositories.ramo_atividade_repository_interface import IRamoAtividadeRepository
from app.infrastructure.repositories.base_repository import BaseRepository


class RamoAtividadeRepositoryImpl(IRamoAtividadeRepository, BaseRepository[RamoAtividade]):
    """Repository para operações de RamoAtividade com CRUD completo"""

    def __init__(self):
        super().__init__(RamoAtividade)

    def create(self, ramo_atividade: RamoAtividade, session: Session) -> RamoAtividade:
        """Cria um novo ramo de atividade"""
        session.add(ramo_atividade)
        session.flush()
        return ramo_atividade

    def get_by_id(self, ramo_id: int, session: Session) -> Optional[RamoAtividade]:
        """Busca ramo de atividade por ID"""
        return session.query(RamoAtividade).filter(RamoAtividade.id == ramo_id).first()

    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[RamoAtividade]:
        """Lista todos os ramos de atividade"""
        return session.query(RamoAtividade).offset(skip).limit(limit).all()

    def update(self, ramo_atividade: RamoAtividade, session: Session) -> RamoAtividade:
        """Atualiza um ramo de atividade"""
        session.merge(ramo_atividade)
        session.flush()
        return ramo_atividade

    def delete(self, ramo_id: int, session: Session) -> bool:
        """Deleta um ramo de atividade"""
        ramo = self.get_by_id(ramo_id, session)
        if ramo:
            session.delete(ramo)
            session.flush()
            return True
        return False

    def exists_by_id(self, ramo_id: int, session: Session) -> bool:
        """Verifica se ramo de atividade existe por ID"""
        return session.query(RamoAtividade).filter(RamoAtividade.id == ramo_id).first() is not None

    def search_by_description(self, description: str, session: Session) -> List[RamoAtividade]:
        """Busca ramos de atividade por descrição"""
        return session.query(RamoAtividade).filter(
            RamoAtividade.descricao.ilike(f"%{description}%")
        ).all()

    def get_by_description(self, description: str, session: Session) -> Optional[RamoAtividade]:
        """Busca ramo de atividade por descrição exata"""
        return session.query(RamoAtividade).filter(RamoAtividade.descricao == description).first()
