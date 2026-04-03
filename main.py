from fastapi import FastAPI
from app.routes import colaboradores, quartos, alocacoes, manutencoes

app = FastAPI(title="Smart Housing API", version="1.0.0")

app.include_router(colaboradores.router)
app.include_router(quartos.router)
app.include_router(alocacoes.router)
app.include_router(manutencoes.router)

@app.get("/")
def home():
    return {"msg": "Smart Housing API rodando no Debian!"}
