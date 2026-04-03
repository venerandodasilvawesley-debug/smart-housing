from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, TIMESTAMP
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    role = Column(String(20), default="user", nullable=False)
    ativo = Column(Boolean, default=True)

class Colaborador(Base):
    __tablename__ = "colaboradores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    documento = Column(String(50), unique=True, nullable=False)
    empresa = Column(String(100))
    setor = Column(String(100))
    ativo = Column(Boolean, default=True)

class Quarto(Base):
    __tablename__ = "quartos"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, nullable=False)
    capacidade = Column(Integer, nullable=False)
    ocupacao_atual = Column(Integer, default=0)

class Alocacao(Base):
    __tablename__ = "alocacoes"
    id = Column(Integer, primary_key=True, index=True)
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id"))
    quarto_id = Column(Integer, ForeignKey("quartos.id"))
    data_entrada = Column(Date, nullable=False)
    data_saida = Column(Date)

class Manutencao(Base):
    __tablename__ = "manutencoes"
    id = Column(Integer, primary_key=True, index=True)
    quarto_id = Column(Integer, ForeignKey("quartos.id"))
    descricao = Column(String, nullable=False)
    status = Column(String(50), default="Aberto")
    data_abertura = Column(TIMESTAMP)
    data_fechamento = Column(TIMESTAMP)
