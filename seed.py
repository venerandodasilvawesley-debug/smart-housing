"""Script para popular o banco com dados iniciais."""
from app.database import SessionLocal
from app import models
from passlib.context import CryptContext
from datetime import date

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed():
    db = SessionLocal()
    try:
        # Usuários
        if not db.query(models.Usuario).filter_by(username="admin").first():
            db.add(models.Usuario(username="admin", hashed_password=pwd_context.hash("admin123"), role="admin"))
        if not db.query(models.Usuario).filter_by(username="operador").first():
            db.add(models.Usuario(username="operador", hashed_password=pwd_context.hash("op123"), role="user"))

        # Quartos
        quartos = [
            models.Quarto(numero=101, capacidade=2),
            models.Quarto(numero=102, capacidade=3),
            models.Quarto(numero=201, capacidade=4),
            models.Quarto(numero=202, capacidade=2),
        ]
        for q in quartos:
            if not db.query(models.Quarto).filter_by(numero=q.numero).first():
                db.add(q)

        db.flush()

        # Colaboradores
        colaboradores = [
            models.Colaborador(nome="Ana Silva", documento="11111111111", empresa="Construtora X", setor="Obras"),
            models.Colaborador(nome="Bruno Costa", documento="22222222222", empresa="Construtora X", setor="Elétrica"),
            models.Colaborador(nome="Carlos Melo", documento="33333333333", empresa="Empresa Y", setor="Hidráulica"),
            models.Colaborador(nome="Diana Ramos", documento="44444444444", empresa="Empresa Y", setor="Obras"),
        ]
        for c in colaboradores:
            if not db.query(models.Colaborador).filter_by(documento=c.documento).first():
                db.add(c)

        db.flush()

        # Alocações
        ana = db.query(models.Colaborador).filter_by(documento="11111111111").first()
        q101 = db.query(models.Quarto).filter_by(numero=101).first()
        if ana and q101 and not db.query(models.Alocacao).filter_by(colaborador_id=ana.id, data_saida=None).first():
            db.add(models.Alocacao(colaborador_id=ana.id, quarto_id=q101.id, data_entrada=date(2026, 1, 10)))
            q101.ocupacao_atual += 1

        # Manutenção
        if q101 and not db.query(models.Manutencao).filter_by(quarto_id=q101.id).first():
            db.add(models.Manutencao(quarto_id=q101.id, descricao="Trocar lâmpada do banheiro", status="Aberto"))

        db.commit()
        print("✅ Seed executado com sucesso!")
    except Exception as e:
        db.rollback()
        print(f"❌ Erro no seed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
