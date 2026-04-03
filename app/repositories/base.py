"""Consultas SQLAlchemy centralizadas."""
from sqlalchemy.orm import Session
from app import models


def get_all(db: Session, model, skip: int = 0, limit: int = 100):
    return db.query(model).offset(skip).limit(limit).all()

def get_by_id(db: Session, model, id: int):
    return db.query(model).filter(model.id == id).first()

def save(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, obj):
    db.delete(obj)
    db.commit()


# ── Específicos ───────────────────────────────────────────────
def get_colaborador_by_documento(db: Session, documento: str):
    return db.query(models.Colaborador).filter(models.Colaborador.documento == documento).first()

def get_quarto_by_numero(db: Session, numero: int):
    return db.query(models.Quarto).filter(models.Quarto.numero == numero).first()

def get_alocacoes_ativas_por_quarto(db: Session, quarto_id: int):
    return db.query(models.Alocacao).filter(
        models.Alocacao.quarto_id == quarto_id,
        models.Alocacao.data_saida == None  # noqa: E711
    ).all()

def get_usuario_by_username(db: Session, username: str):
    return db.query(models.Usuario).filter(models.Usuario.username == username).first()
