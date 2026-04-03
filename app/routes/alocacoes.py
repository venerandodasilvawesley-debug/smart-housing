from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/alocacoes", tags=["Alocações"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    if not crud.get_colaborador(db, data.colaborador_id):
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    if not crud.get_quarto(db, data.quarto_id):
        raise HTTPException(status_code=404, detail="Quarto não encontrado")
    return crud.create_alocacao(db, data)

@router.put("/{alocacao_id}", response_model=schemas.AlocacaoRead)
def atualizar_alocacao(alocacao_id: int, data: schemas.AlocacaoUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.update_alocacao(db, alocacao_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Alocação não encontrada")
    return obj

@router.delete("/{alocacao_id}")
def deletar_alocacao(alocacao_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.delete_alocacao(db, alocacao_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Alocação não encontrada")
    return {"msg": "Alocação deletada com sucesso"}
