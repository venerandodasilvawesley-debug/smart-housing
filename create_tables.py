from app.database import engine, Base
from app import models

print("Criando tabelas no banco...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
