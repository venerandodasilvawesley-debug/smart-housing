import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.database import engine
from app import models
from app.routes import colaboradores, quartos, alocacoes, manutencoes, auth

models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart Housing API",
    version="1.0.0",
    description=(
        "API para gerenciamento de alojamentos de colaboradores.\n\n"
        "## Autenticação\n"
        "Use `POST /auth/token` para obter um Bearer Token e clique em **Authorize** acima.\n\n"
        "## Permissões\n"
        "- **user** — leitura e criação em todos os recursos\n"
        "- **admin** — inclui operações de exclusão"
    ),
    contact={"name": "Smart Housing", "url": "https://github.com/venerandodasilvawesley-debug/smart-housing"},
)


<<<<<<< HEAD

=======
>>>>>>> d2d39ab11b1ac8d67f5285f54899049eb9d202d5
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(colaboradores.router)
app.include_router(quartos.router)
app.include_router(alocacoes.router)
app.include_router(manutencoes.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    safe_errors = []
    for e in exc.errors():
        safe_e = {k: v for k, v in e.items() if k != "input"}
        if "ctx" in safe_e:
            safe_e["ctx"] = {k: str(v) for k, v in safe_e["ctx"].items()}
        safe_errors.append(safe_e)
    return JSONResponse(status_code=422, content={"detail": "Dados de entrada inválidos", "errors": safe_errors})


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Erro não tratado: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Erro interno do servidor."})


@app.get("/")
def home():
    return {"msg": "Smart Housing API rodando no Debian!"}
