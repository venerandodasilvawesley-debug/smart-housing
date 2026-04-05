# 🏠 Smart Housing API

API RESTful para gerenciamento de alojamentos de colaboradores, construída com **FastAPI** e **PostgreSQL**.

---

## 🚀 Subindo com Docker (recomendado)

```bash
git clone https://github.com/venerandodasilvawesley-debug/smart-housing.git
cd smart-housing

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com sua SECRET_KEY e credenciais do banco

# Suba a API + PostgreSQL
docker compose up --build
```

A API estará disponível em **http://localhost:8000**
Documentação Swagger: **http://localhost:8000/docs**

> O banco é criado automaticamente via `alembic upgrade head` e populado com dados iniciais via `seed.py`.

---

## 🛠️ Instalação local (sem Docker)

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edite .env com DATABASE_URL, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

alembic upgrade head   # cria tabelas
python seed.py         # dados iniciais (opcional)
uvicorn main:app --reload
```

---

## 🔑 Autenticação

A API usa **JWT Bearer Token**. Para obter um token:

```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

Use o token retornado no header de todas as requisições:
```
Authorization: Bearer <token>
```

### Usuários criados pelo seed

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | admin |
| `operador` | `op123` | user |

---

## 📋 Endpoints

### Autenticação
| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/register` | Registrar novo usuário |
| POST | `/auth/token` | Login — retorna JWT |

### Colaboradores
| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/colaboradores/` | user | Listar todos |
| GET | `/colaboradores/{id}` | user | Buscar por ID |
| POST | `/colaboradores/` | user | Criar colaborador |
| PUT | `/colaboradores/{id}` | user | Atualizar colaborador |
| DELETE | `/colaboradores/{id}` | **admin** | Remover colaborador |

### Quartos
| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/quartos/` | user | Listar todos |
| GET | `/quartos/{id}` | user | Buscar por ID |
| POST | `/quartos/` | user | Criar quarto |
| PUT | `/quartos/{id}` | user | Atualizar quarto |
| DELETE | `/quartos/{id}` | **admin** | Remover quarto |

### Alocações
| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/alocacoes/` | user | Listar todas |
| GET | `/alocacoes/{id}` | user | Buscar por ID |
| POST | `/alocacoes/` | user | Alocar colaborador em quarto |
| PUT | `/alocacoes/{id}` | user | Atualizar data de saída |
| DELETE | `/alocacoes/{id}` | **admin** | Desalocar colaborador |

### Manutenções
| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/manutencoes/` | user | Listar todas |
| GET | `/manutencoes/{id}` | user | Buscar por ID |
| POST | `/manutencoes/` | user | Abrir chamado de manutenção |
| PUT | `/manutencoes/{id}` | user | Atualizar status/descrição |
| DELETE | `/manutencoes/{id}` | **admin** | Remover manutenção |

---

## 🧪 Testes

```bash
pytest tests/ -v   # 41 testes
```

---

## 🐳 Variáveis de ambiente

| Variável | Descrição | Exemplo |
|---|---|---|
| `DATABASE_URL` | URL de conexão PostgreSQL | `postgresql://user:pass@localhost:5432/db` |
| `SECRET_KEY` | Chave secreta JWT (use valor longo e aleatório) | `openssl rand -hex 32` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração do token em minutos | `60` |
| `POSTGRES_USER` | Usuário do Postgres (Docker) | `wesley` |
| `POSTGRES_PASSWORD` | Senha do Postgres (Docker) | `senha_forte` |
| `POSTGRES_DB` | Nome do banco (Docker) | `smart_housing` |

---

## 🏗️ Estrutura do projeto

```
smart_housing/
├── main.py                  # entrypoint FastAPI
├── app/
│   ├── models.py            # modelos SQLAlchemy
│   ├── schemas.py           # schemas Pydantic
│   ├── crud.py              # operações de banco
│   ├── auth.py              # JWT + dependências de auth
│   ├── database.py          # engine, sessão, Base
│   ├── routes/              # endpoints por recurso
│   ├── services/            # regras de negócio
│   └── repositories/        # queries centralizadas
├── alembic/                 # migrations
├── tests/                   # testes pytest
├── Dockerfile
└── docker-compose.yml
```

