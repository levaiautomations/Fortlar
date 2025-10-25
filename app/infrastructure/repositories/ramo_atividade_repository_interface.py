from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.models.ramo_atividade_model import RamoAtividade
from app.infrastructure.configs.database_config import Session


class IRamoAtividadeRepository(ABC):
    """Interface para operações de RamoAtividade"""

    @abstractmethod
    def create(self, ramo_atividade: RamoAtividade, session: Session) -> RamoAtividade:
        """Cria um novo ramo de atividade"""
        pass

    @abstractmethod
    def get_by_id(self, ramo_id: int, session: Session) -> Optional[RamoAtividade]:
        """Busca ramo de atividade por ID"""
        pass

    @abstractmethod
    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[RamoAtividade]:
        """Lista todos os ramos de atividade"""
        pass

    @abstractmethod
    def update(self, ramo_atividade: RamoAtividade, session: Session) -> RamoAtividade:
        """Atualiza um ramo de atividade"""
        pass

    @abstractmethod
    def delete(self, ramo_id: int, session: Session) -> bool:
        """Deleta um ramo de atividade"""
        pass

    @abstractmethod
    def exists_by_id(self, ramo_id: int, session: Session) -> bool:
        """Verifica se ramo de atividade existe por ID"""
        pass

    @abstractmethod
    def search_by_description(self, description: str, session: Session) -> List[RamoAtividade]:
        """Busca ramos de atividade por descrição"""
        pass

    @abstractmethod
    def get_by_description(self, description: str, session: Session) -> Optional[RamoAtividade]:
        """Busca ramo de atividade por descrição exata"""
        pass
