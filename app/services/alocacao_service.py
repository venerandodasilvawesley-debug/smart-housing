"""Regras de negócio para alocações."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.repositories import base as repo
from datetime import datetime


def alocar_colaborador(db: Session, data: schemas.AlocacaoCreate) -> models.Alocacao:
    colaborador = repo.get_by_id(db, models.Colaborador, data.colaborador_id)
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")

    quarto = repo.get_by_id(db, models.Quarto, data.quarto_id)
    if not quarto:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")

    if quarto.ocupacao_atual >= quarto.capacidade:
        raise HTTPException(
            status_code=409,
            detail=f"Quarto {quarto.numero} está cheio ({quarto.ocupacao_atual}/{quarto.capacidade})"
        )

    alocacoes_ativas = repo.get_alocacoes_ativas_por_quarto(db, data.quarto_id)
    if len(alocacoes_ativas) >= quarto.capacidade:
        raise HTTPException(status_code=409, detail="Quarto sem vagas disponíveis")

    alocacao = models.Alocacao(**data.model_dump())
    quarto.ocupacao_atual += 1
    return repo.save(db, alocacao)


def desalocar_colaborador(db: Session, alocacao_id: int) -> dict:
    alocacao = repo.get_by_id(db, models.Alocacao, alocacao_id)
    if not alocacao:
        raise HTTPException(status_code=404, detail="Alocação não encontrada")

    quarto = repo.get_by_id(db, models.Quarto, alocacao.quarto_id)
    if quarto and quarto.ocupacao_atual > 0:
        quarto.ocupacao_atual -= 1

    repo.delete(db, alocacao)
    return {"msg": "Colaborador desalocado com sucesso"}
