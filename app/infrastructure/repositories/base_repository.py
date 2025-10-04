"""Repository base com operações CRUD genéricas"""

from typing import TypeVar, Generic, List, Optional, Type, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.infrastructure.configs.database_config import Session

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Repository base com operações CRUD genéricas"""
    
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
    
    def create(self, entity: T, session: Session) -> T:
        """Cria uma nova entidade"""
        session.add(entity)
        session.flush()
        session.refresh(entity)
        return entity
    
    def get_by_id(self, entity_id: int, session: Session) -> Optional[T]:
        """Busca entidade por ID"""
        return session.query(self.model_class).filter(
            self.model_class.id == entity_id
        ).first()
    
    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[T]:
        """Busca todas as entidades com paginação"""
        return session.query(self.model_class).offset(skip).limit(limit).all()
    
    def update(self, entity: T, session: Session) -> T:
        """Atualiza uma entidade existente"""
        session.flush()
        session.refresh(entity)
        return entity
    
    def delete(self, entity_id: int, session: Session) -> bool:
        """Deleta uma entidade por ID"""
        entity = self.get_by_id(entity_id, session)
        if entity:
            session.delete(entity)
            return True
        return False
    
    def exists_by_id(self, entity_id: int, session: Session) -> bool:
        """Verifica se entidade existe por ID"""
        return session.query(self.model_class).filter(
            self.model_class.id == entity_id
        ).first() is not None
    
    def count(self, session: Session) -> int:
        """Conta total de entidades"""
        return session.query(self.model_class).count()
    
    def find_by_filters(self, filters: Dict[str, Any], session: Session) -> List[T]:
        """Busca entidades por filtros"""
        query = session.query(self.model_class)
        
        for field, value in filters.items():
            if hasattr(self.model_class, field):
                query = query.filter(getattr(self.model_class, field) == value)
        
        return query.all()
    
    def find_one_by_filters(self, filters: Dict[str, Any], session: Session) -> Optional[T]:
        """Busca uma entidade por filtros"""
        query = session.query(self.model_class)
        
        for field, value in filters.items():
            if hasattr(self.model_class, field):
                query = query.filter(getattr(self.model_class, field) == value)
        
        return query.first()
