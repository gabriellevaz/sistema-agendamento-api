from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
import re

class CompanyBase(BaseModel):
    name: str
    slug: str
    cnpj: str
    service_type: str
    parent_company_id: Optional[str] = None
    is_active: int = 1

    # Validação automática para garantir que o slug seja sempre minúsculo e sem espaços
    @field_validator('slug')
    @classmethod
    def slug_must_be_kebab_case(cls, v: str) -> str:
        # Remove caracteres especiais e troca espaços por hífens
        v = v.lower().strip()
        return re.sub(r'[^a-z0-9\-]', '', v.replace(' ', '-'))

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)