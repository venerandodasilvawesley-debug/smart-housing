from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter(prefix="/colaboradores", tags=["Colaboradores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.ColaboradorRead])
def listar_colaboradores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_colaboradores(db, skip=skip, limit=limit)

@router.get("/{colaborador_id}", response_model=schemas.ColaboradorRead)
def buscar_colaborador(colaborador_id: int, db: Session = Depends(get_db)):
    obj = crud.get_colaborador(db, colaborador_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return obj

@router.post("/", response_model=schemas.ColaboradorRead, status_code=201)
def criar_colaborador(data: schemas.ColaboradorCreate, db: Session = Depends(get_db)):
    return crud.create_colaborador(db, data)

@router.put("/{colaborador_id}", response_model=schemas.ColaboradorRead)
def atualizar_colaborador(colaborador_id: int, data: schemas.ColaboradorUpdate, db: Session = Depends(get_db)):
    obj = crud.update_colaborador(db, colaborador_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return obj

@router.delete("/{colaborador_id}")
def deletar_colaborador(colaborador_id: int, db: Session = Depends(get_db)):
    obj = crud.delete_colaborador(db, colaborador_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return {"msg": "Colaborador deletado com sucesso"}
