from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cria a engine do SQLite - hospital.db
engine = create_engine('sqlite:///hospital.db', echo=True)

# Cria a sessão para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função auxiliar para obter uma sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()