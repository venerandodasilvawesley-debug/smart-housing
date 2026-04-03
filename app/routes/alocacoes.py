from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter(prefix="/alocacoes", tags=["Alocações"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.AlocacaoRead])
def listar_alocacoes(db: Session = Depends(get_db)):
    return crud.get_alocacoes(db)

@router.get("/{alocacao_id}", response_model=schemas.AlocacaoRead)
def buscar_alocacao(alocacao_id: int, db: Session = Depends(get_db)):
    obj = crud.get_alocacao(db, alocacao_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Alocação não encontrada")
    return obj

@router.post("/", response_model=schemas.AlocacaoRead, status_code=201)
def criar_alocacao(data: schemas.AlocacaoCreate, db: Session = Depends(get_db)):
    return crud.create_alocacao(db, data)

@router.put("/{alocacao_id}", response_model=schemas.AlocacaoRead)
def atualizar_alocacao(alocacao_id: int, data: schemas.AlocacaoUpdate, db: Session = Depends(get_db)):
    obj = crud.update_alocacao(db, alocacao_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Alocação não encontrada")
    return obj

@router.delete("/{alocacao_id}")
def deletar_alocacao(alocacao_id: int, db: Session = Depends(get_db)):
    obj = crud.delete_alocacao(db, alocacao_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Alocação não encontrada")
    return {"msg": "Alocação deletada com sucesso"}
