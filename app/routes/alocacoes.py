from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from app.auth import get_current_user, require_admin
from app.services import alocacao_service

router = APIRouter(prefix="/alocacoes", tags=["Alocações"])


@router.get("/", response_model=list[schemas.AlocacaoRead])
def listar_alocacoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return crud.get_alocacoes(db, skip=skip, limit=limit)

@router.get("/{alocacao_id}", response_model=schemas.AlocacaoRead)
def buscar_alocacao(alocacao_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.get_alocacao(db, alocacao_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Alocação não encontrada")
    return obj

@router.post("/", response_model=schemas.AlocacaoRead, status_code=201)
def criar_alocacao(data: schemas.AlocacaoCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return alocacao_service.alocar_colaborador(db, data)

@router.put("/{alocacao_id}", response_model=schemas.AlocacaoRead)
def atualizar_alocacao(alocacao_id: int, data: schemas.AlocacaoUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.update_alocacao(db, alocacao_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Alocação não encontrada")
    return obj

@router.delete("/{alocacao_id}")
def deletar_alocacao(alocacao_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    return alocacao_service.desalocar_colaborador(db, alocacao_id)
