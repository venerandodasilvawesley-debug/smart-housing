from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional
from datetime import date, datetime


# ── Autenticação ─────────────────────────────────────────────
class UsuarioCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)
    role: str = Field(default="user", pattern="^(admin|user)$")

class UsuarioRead(BaseModel):
    id: int
    username: str
    role: str
    ativo: bool
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Colaborador ──────────────────────────────────────────────
class ColaboradorBase(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    documento: str = Field(min_length=5, max_length=50)
    empresa: Optional[str] = Field(None, max_length=100)
    setor: Optional[str] = Field(None, max_length=100)
    ativo: Optional[bool] = True

class ColaboradorCreate(ColaboradorBase):
    pass

class ColaboradorUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    documento: Optional[str] = Field(None, min_length=5, max_length=50)
    empresa: Optional[str] = Field(None, max_length=100)
    setor: Optional[str] = Field(None, max_length=100)
    ativo: Optional[bool] = None

class ColaboradorRead(ColaboradorBase):
    id: int
    model_config = {"from_attributes": True}


# ── Quarto ───────────────────────────────────────────────────
class QuartoBase(BaseModel):
    numero: int = Field(gt=0)
    capacidade: int = Field(gt=0, le=500)
    ocupacao_atual: Optional[int] = Field(0, ge=0, le=500)

class QuartoCreate(QuartoBase):
    pass

class QuartoUpdate(BaseModel):
    numero: Optional[int] = Field(None, gt=0)
    capacidade: Optional[int] = Field(None, gt=0, le=500)
    ocupacao_atual: Optional[int] = Field(None, ge=0, le=500)

class QuartoRead(QuartoBase):
    id: int
    model_config = {"from_attributes": True}


# ── Alocacao ─────────────────────────────────────────────────
class AlocacaoBase(BaseModel):
    colaborador_id: int = Field(gt=0)
    quarto_id: int = Field(gt=0)
    data_entrada: date
    data_saida: Optional[date] = None

class AlocacaoCreate(AlocacaoBase):
    @model_validator(mode="after")
    def validar_datas(self):
        if self.data_saida and self.data_saida < self.data_entrada:
            raise ValueError("data_saida deve ser igual ou posterior a data_entrada")
        return self

class AlocacaoUpdate(BaseModel):
    data_saida: Optional[date] = None

class AlocacaoRead(AlocacaoBase):
    id: int
    model_config = {"from_attributes": True}


# ── Manutencao ───────────────────────────────────────────────
STATUS_MANUTENCAO = Literal["Aberto", "Em andamento", "Fechado"]

class ManutencaoBase(BaseModel):
    quarto_id: int = Field(gt=0)
    descricao: str = Field(min_length=5, max_length=500)
    status: Optional[STATUS_MANUTENCAO] = "Aberto"

class ManutencaoCreate(ManutencaoBase):
    pass

class ManutencaoUpdate(BaseModel):
    descricao: Optional[str] = Field(None, min_length=5, max_length=500)
    status: Optional[STATUS_MANUTENCAO] = None
    data_fechamento: Optional[datetime] = None

class ManutencaoRead(ManutencaoBase):
    id: int
    data_abertura: Optional[datetime] = None
    data_fechamento: Optional[datetime] = None
    model_config = {"from_attributes": True}
