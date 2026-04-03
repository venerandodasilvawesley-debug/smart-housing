from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter(prefix="/quartos", tags=["Quartos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.QuartoRead])
def listar_quartos(db: Session = Depends(get_db)):
    return crud.get_quartos(db)

@router.get("/{quarto_id}", response_model=schemas.QuartoRead)
def buscar_quarto(quarto_id: int, db: Session = Depends(get_db)):
    obj = crud.get_quarto(db, quarto_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")
    return obj

@router.post("/", response_model=schemas.QuartoRead, status_code=201)
def criar_quarto(data: schemas.QuartoCreate, db: Session = Depends(get_db)):
    return crud.create_quarto(db, data)

@router.put("/{quarto_id}", response_model=schemas.QuartoRead)
def atualizar_quarto(quarto_id: int, data: schemas.QuartoUpdate, db: Session = Depends(get_db)):
    obj = crud.update_quarto(db, quarto_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")
    return obj

@router.delete("/{quarto_id}")
def deletar_quarto(quarto_id: int, db: Session = Depends(get_db)):
    obj = crud.delete_quarto(db, quarto_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")
    return {"msg": "Quarto deletado com sucesso"}
