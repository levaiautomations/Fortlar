"""Service de domínio para lógica de negócio relacionada a empresas"""

from typing import Optional
from app.domain.models.company_model import Company
from app.domain.models.enumerations.role_enumerations import RoleEnum


class CompanyDomainService:
    """Service de domínio para operações de negócio relacionadas a empresas"""
    
    @staticmethod
    def create_company(
        cnpj: str,
        razao_social: str,
        nome_fantasia: str,
        senha_hash: str,
        id_vendedor: int,
        perfil: RoleEnum = RoleEnum.CLIENTE,
        ativo: bool = False
    ) -> Company:
        """Cria uma nova instância de empresa com validações de domínio"""
        return Company(
            id_empresa=None,
            cnpj=cnpj,
            razao_social=razao_social,
            nome_fantasia=nome_fantasia,
            senha_hash=senha_hash,
            perfil=perfil,
            ativo=ativo,
            id_vendedor=id_vendedor
        )
    
    @staticmethod
    def is_company_active(company: Company) -> bool:
        """Verifica se a empresa está ativa"""
        return company.ativo
    
    @staticmethod
    def activate_company(company: Company) -> None:
        """Ativa uma empresa"""
        company.ativo = True
    
    @staticmethod
    def deactivate_company(company: Company) -> None:
        """Desativa uma empresa"""
        company.ativo = False
    
    @staticmethod
    def can_login(company: Company) -> bool:
        """Verifica se a empresa pode fazer login (está ativa)"""
        return company.ativo
    
    @staticmethod
    def has_role(company: Company, required_role: RoleEnum) -> bool:
        """Verifica se a empresa tem o perfil necessário"""
        return company.perfil == required_role
