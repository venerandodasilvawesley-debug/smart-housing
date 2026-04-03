from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter(prefix="/manutencoes", tags=["Manutenções"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.ManutencaoRead])
def listar_manutencoes(db: Session = Depends(get_db)):
    return crud.get_manutencoes(db)

@router.get("/{manutencao_id}", response_model=schemas.ManutencaoRead)
def buscar_manutencao(manutencao_id: int, db: Session = Depends(get_db)):
    obj = crud.get_manutencao(db, manutencao_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")
    return obj

@router.post("/", response_model=schemas.ManutencaoRead, status_code=201)
def criar_manutencao(data: schemas.ManutencaoCreate, db: Session = Depends(get_db)):
    return crud.create_manutencao(db, data)

@router.put("/{manutencao_id}", response_model=schemas.ManutencaoRead)
def atualizar_manutencao(manutencao_id: int, data: schemas.ManutencaoUpdate, db: Session = Depends(get_db)):
    obj = crud.update_manutencao(db, manutencao_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")
    return obj

@router.delete("/{manutencao_id}")
def deletar_manutencao(manutencao_id: int, db: Session = Depends(get_db)):
    obj = crud.delete_manutencao(db, manutencao_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")
    return {"msg": "Manutenção deletada com sucesso"}
