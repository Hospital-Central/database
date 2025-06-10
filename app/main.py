import sys
import os

# Ajusta sys.path para encontrar o pacote database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))

from sqlalchemy.orm import Session
from database.setup import SessionLocal, engine, Base
from database.models import *
from database.procedures import (  
    create_paciente, create_funcionario, create_leito,
    create_internacao, create_agendamento,
    get_paciente_by_id, list_pacientes
)
import datetime

def main():
    # Cria as tabelas se não existirem
    Base.metadata.create_all(bind=engine)

    # Abre sessão
    db: Session = SessionLocal()

    try:
        # Criar paciente
        paciente = create_paciente(db, "João Silva", datetime.date(1980, 5, 15), "12345678900", "999999999", "Rua A, 123")
        print(f"Paciente criado: {paciente.id} - {paciente.nome}")

        # Criar funcionário
        funcionario = create_funcionario(db, "Dra. Ana", "Médica", "Cardiologista", "CRM12345", "988888888")
        print(f"Funcionário criado: {funcionario.id} - {funcionario.nome}")

        # Criar leito
        leito = create_leito(db, "101", "UTI")
        print(f"Leito criado: {leito.id} - {leito.numero} - Disponível? {leito.disponivel}")

        # Criar internação (disponibilidade do leito deve mudar)
        internacao = create_internacao(db, paciente.id, leito.id, datetime.date.today())
        db.refresh(leito)  # Atualiza o objeto leito para pegar alterações no DB
        print(f"Internação criada: {internacao.id} - Leito disponível? {leito.disponivel}")


        # Criar agendamento (gera fatura automaticamente)
        agendamento = create_agendamento(db, paciente.id, funcionario.id, datetime.datetime.now(), "Consulta")
        print(f"Agendamento criado: {agendamento.id}")

        # Listar pacientes para verificar
        pacientes = list_pacientes(db)
        print(f"Pacientes no banco: {[p.nome for p in pacientes]}")

    except Exception as e:
        print(f"Erro durante teste: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    main()
