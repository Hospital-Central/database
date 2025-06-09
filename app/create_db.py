from database.setup import engine, Base 
from database.models import *

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    print("Banco de dados e tabelas criados.")
