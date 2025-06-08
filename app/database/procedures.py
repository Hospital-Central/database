from sqlalchemy.orm import Session
from setup import SessionLocal
from models import (
    Paciente, Funcionario, Consulta, Internacao, Leito,
    Exame, Agendamento, Fatura, Prescricao, Medicamento, PrescricaoMedicamento
)

# 1. Criar paciente
def create_paciente(db: Session, nome: str, data_nascimento, cpf: str, telefone: str, endereco: str):
    paciente = Paciente(nome=nome, data_nascimento=data_nascimento, cpf=cpf, telefone=telefone, endereco=endereco)
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente

# 2. Buscar paciente por ID
def get_paciente_by_id(db: Session, paciente_id: int):
    return db.query(Paciente).filter(Paciente.id == paciente_id).first()

# 3. Listar todos os pacientes
def list_pacientes(db: Session):
    return db.query(Paciente).all()

# 4. Criar funcionário
def create_funcionario(db: Session, nome: str, cargo: str, especialidade: str, crm: str, telefone: str):
    funcionario = Funcionario(nome=nome, cargo=cargo, especialidade=especialidade, crm=crm, telefone=telefone)
    db.add(funcionario)
    db.commit()
    db.refresh(funcionario)
    return funcionario

# 5. Criar consulta
def create_consulta(db: Session, id_paciente: int, id_funcionario: int, data_hora):
    consulta = Consulta(id_paciente=id_paciente, id_funcionario=id_funcionario, data_hora=data_hora)
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta

# 6. Criar internação
def create_internacao(db: Session, id_paciente: int, id_leito: int, data_entrada, data_saida=None):
    internacao = Internacao(id_paciente=id_paciente, id_leito=id_leito, data_entrada=data_entrada, data_saida=data_saida)
    db.add(internacao)
    db.commit()
    db.refresh(internacao)
    return internacao

# 7. Criar leito
def create_leito(db: Session, numero: str, tipo: str, disponivel: bool = True):
    leito = Leito(numero=numero, tipo=tipo, disponivel=disponivel)
    db.add(leito)
    db.commit()
    db.refresh(leito)
    return leito

# 8. Criar exame
def create_exame(db: Session, id_paciente: int, id_funcionario: int, tipo: str, resultado: str, data):
    exame = Exame(tipo=tipo, resultado=resultado, data=data, id_paciente=id_paciente, id_funcionario=id_funcionario)
    db.add(exame)
    db.commit()
    db.refresh(exame)
    return exame

# 9. Criar agendamento
def create_agendamento(db: Session, id_paciente: int, id_funcionario: int, data_hora, tipo: str):
    agendamento = Agendamento(data_hora=data_hora, tipo=tipo, paciente_id=id_paciente, funcionario_id=id_funcionario)
    db.add(agendamento)
    db.commit()
    db.refresh(agendamento)
    return agendamento

# 10. Criar fatura
def create_fatura(db: Session, id_paciente: int, id_funcionario: int, data_emissao, valor: float, status_pag: str):
    fatura = Fatura(data_emissao=data_emissao, valor=valor, status_pag=status_pag, paciente_id=id_paciente, funcionario_id=id_funcionario)
    db.add(fatura)
    db.commit()
    db.refresh(fatura)
    return fatura

# 11. Criar prescrição
def create_prescricao(db: Session, id_paciente: int, id_funcionario: int, data_prescricao):
    prescricao = Prescricao(data_prescricao=data_prescricao, paciente_id=id_paciente, funcionario_id=id_funcionario)
    db.add(prescricao)
    db.commit()
    db.refresh(prescricao)
    return prescricao

# 12. Associar medicamento à prescrição
def add_medicamento_prescricao(db: Session, id_prescricao: int, id_medicamento: int, quantidade: int, instrucoes: str):
    assoc = PrescricaoMedicamento(id_prescricao=id_prescricao, id_medicamento=id_medicamento, quantidade=quantidade, instrucoes=instrucoes)
    db.add(assoc)
    db.commit()
    db.refresh(assoc)
    return assoc

