from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from app.auth import get_current_user, require_admin

router = APIRouter(prefix="/manutencoes", tags=["Manutenções"])


@router.get("/", response_model=list[schemas.ManutencaoRead])
def listar_manutencoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return crud.get_manutencoes(db, skip=skip, limit=limit)

@router.get("/{manutencao_id}", response_model=schemas.ManutencaoRead)
def buscar_manutencao(manutencao_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.get_manutencao(db, manutencao_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")
    return obj

@router.post("/", response_model=schemas.ManutencaoRead, status_code=201)
def criar_manutencao(data: schemas.ManutencaoCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return crud.create_manutencao(db, data)

@router.put("/{manutencao_id}", response_model=schemas.ManutencaoRead)
def atualizar_manutencao(manutencao_id: int, data: schemas.ManutencaoUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.update_manutencao(db, manutencao_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")
    return obj

@router.delete("/{manutencao_id}")
def deletar_manutencao(manutencao_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    obj = crud.delete_manutencao(db, manutencao_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")
    return {"msg": "Manutenção deletada com sucesso"}
