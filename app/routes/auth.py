from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, schemas
from app.auth import create_access_token, get_db

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=schemas.UsuarioRead, status_code=201)
def registrar(data: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if crud.get_usuario_by_username(db, data.username):
        raise HTTPException(status_code=400, detail="Username já cadastrado")
    return crud.create_usuario(db, data)


@router.post("/token", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_usuario_by_username(db, form.username)
    if not user or not crud.verificar_senha(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
