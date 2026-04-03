from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas


# ── Colaboradores ────────────────────────────────────────────
def get_colaboradores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Colaborador).offset(skip).limit(limit).all()

def get_colaborador(db: Session, colaborador_id: int):
    return db.query(models.Colaborador).filter(models.Colaborador.id == colaborador_id).first()

def create_colaborador(db: Session, data: schemas.ColaboradorCreate):
    obj = models.Colaborador(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_colaborador(db: Session, colaborador_id: int, data: schemas.ColaboradorUpdate):
    obj = get_colaborador(db, colaborador_id)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_colaborador(db: Session, colaborador_id: int):
    obj = get_colaborador(db, colaborador_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


# ── Quartos ──────────────────────────────────────────────────
def get_quartos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Quarto).offset(skip).limit(limit).all()

def get_quarto(db: Session, quarto_id: int):
    return db.query(models.Quarto).filter(models.Quarto.id == quarto_id).first()

def create_quarto(db: Session, data: schemas.QuartoCreate):
    obj = models.Quarto(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_quarto(db: Session, quarto_id: int, data: schemas.QuartoUpdate):
    obj = get_quarto(db, quarto_id)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_quarto(db: Session, quarto_id: int):
    obj = get_quarto(db, quarto_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


# ── Alocacoes ────────────────────────────────────────────────
def get_alocacoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Alocacao).offset(skip).limit(limit).all()

def get_alocacao(db: Session, alocacao_id: int):
    return db.query(models.Alocacao).filter(models.Alocacao.id == alocacao_id).first()

def create_alocacao(db: Session, data: schemas.AlocacaoCreate):
    obj = models.Alocacao(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_alocacao(db: Session, alocacao_id: int, data: schemas.AlocacaoUpdate):
    obj = get_alocacao(db, alocacao_id)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_alocacao(db: Session, alocacao_id: int):
    obj = get_alocacao(db, alocacao_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


# ── Manutencoes ──────────────────────────────────────────────
def get_manutencoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Manutencao).offset(skip).limit(limit).all()

def get_manutencao(db: Session, manutencao_id: int):
    return db.query(models.Manutencao).filter(models.Manutencao.id == manutencao_id).first()

def create_manutencao(db: Session, data: schemas.ManutencaoCreate):
    obj = models.Manutencao(**data.model_dump(), data_abertura=datetime.now())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_manutencao(db: Session, manutencao_id: int, data: schemas.ManutencaoUpdate):
    obj = get_manutencao(db, manutencao_id)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_manutencao(db: Session, manutencao_id: int):
    obj = get_manutencao(db, manutencao_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
