from pydantic import BaseModel, ConfigDict
from typing import Optional

# 1. Base: Os campos comuns que usamos tanto para criar quanto para ler
class CompanyBase(BaseModel):
    name: str
    slug: str
    cnpj: str
    service_type: str
    parent_company_id: Optional[str] = None
    is_active: int = 1

# 2. Create: O que exigimos que o Frontend nos envie para CRIAR uma empresa
class CompanyCreate(CompanyBase):
    pass # Por enquanto, é igual à base

# 3. Response: O que nós devolvemos para o Frontend depois de criar ou buscar
class CompanyResponse(CompanyBase):
    id: str
    created_at: str

    # Isso avisa ao Pydantic para saber ler os dados do SQLAlchemy (ORM)
    model_config = ConfigDict(from_attributes=True)