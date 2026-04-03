# Smart Housing API

API RESTful para gerenciamento de alojamentos de colaboradores, construída com **FastAPI** e **PostgreSQL**.

## Tecnologias
- Python 3 + FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Pydantic v2
- python-dotenv

## Instalação

```bash
# Clone o repositório
git clone https://github.com/venerandodasilvawesley-debug/smart-housing.git
cd smart-housing

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate

# Instale as dependências
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv

# Configure o banco de dados
cp .env.example .env
# Edite o .env com suas credenciais

# Crie as tabelas
python create_tables.py

# Inicie a API
uvicorn main:app --reload
```

## Variáveis de ambiente

Crie um arquivo `.env` com base no `.env.example`:

```
DATABASE_URL=postgresql://usuario:senha@localhost:5432/smart_housing
```

## Endpoints

| Recurso | Métodos |
|---|---|
| `/colaboradores` | GET, POST, GET/{id}, PUT/{id}, DELETE/{id} |
| `/quartos` | GET, POST, GET/{id}, PUT/{id}, DELETE/{id} |
| `/alocacoes` | GET, POST, GET/{id}, PUT/{id}, DELETE/{id} |
| `/manutencoes` | GET, POST, GET/{id}, PUT/{id}, DELETE/{id} |

Documentação interativa disponível em: `http://localhost:8000/docs`
