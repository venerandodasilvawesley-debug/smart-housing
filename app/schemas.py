from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


# ── Colaborador ──────────────────────────────────────────────
class ColaboradorBase(BaseModel):
    nome: str
    documento: str
    empresa: Optional[str] = None
    setor: Optional[str] = None
    ativo: Optional[bool] = True

class ColaboradorCreate(ColaboradorBase):
    pass

class ColaboradorUpdate(BaseModel):
    nome: Optional[str] = None
    empresa: Optional[str] = None
    setor: Optional[str] = None
    ativo: Optional[bool] = None

class ColaboradorRead(ColaboradorBase):
    id: int
    class Config:
        from_attributes = True


# ── Quarto ───────────────────────────────────────────────────
class QuartoBase(BaseModel):
    numero: int
    capacidade: int
    ocupacao_atual: Optional[int] = 0

class QuartoCreate(QuartoBase):
    pass

class QuartoUpdate(BaseModel):
    numero: Optional[int] = None
    capacidade: Optional[int] = None
    ocupacao_atual: Optional[int] = None

class QuartoRead(QuartoBase):
    id: int
    class Config:
        from_attributes = True


# ── Alocacao ─────────────────────────────────────────────────
class AlocacaoBase(BaseModel):
    colaborador_id: int
    quarto_id: int
    data_entrada: date
    data_saida: Optional[date] = None

class AlocacaoCreate(AlocacaoBase):
    pass

class AlocacaoUpdate(BaseModel):
    data_saida: Optional[date] = None

class AlocacaoRead(AlocacaoBase):
    id: int
    class Config:
        from_attributes = True


# ── Manutencao ───────────────────────────────────────────────
class ManutencaoBase(BaseModel):
    quarto_id: int
    descricao: str
    status: Optional[str] = "Aberto"

class ManutencaoCreate(ManutencaoBase):
    pass

class ManutencaoUpdate(BaseModel):
    descricao: Optional[str] = None
    status: Optional[str] = None
    data_fechamento: Optional[datetime] = None

class ManutencaoRead(ManutencaoBase):
    id: int
    data_abertura: Optional[datetime] = None
    data_fechamento: Optional[datetime] = None
    class Config:
        from_attributes = True
