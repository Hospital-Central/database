from sqlalchemy.orm import Session
from database.models import (
    Paciente, Funcionario, Consulta, Internacao, Leito,
    Exame, Agendamento, Fatura, Prescricao, Medicamento, PrescricaoMedicamento
)
from database.triggers import marcar_leito_indisponivel, gerar_fatura_automatica


def create_paciente(db: Session, nome: str, data_nascimento, cpf: str, telefone: str, endereco: str):
    paciente = Paciente(nome=nome, data_nascimento=data_nascimento, cpf=cpf, telefone=telefone, endereco=endereco)
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente


def get_paciente_by_id(db: Session, paciente_id: int):
    return db.query(Paciente).filter(Paciente.id == paciente_id).first()


def list_pacientes(db: Session):
    return db.query(Paciente).all()


def create_funcionario(db: Session, nome: str, cargo: str, especialidade: str, crm: str, telefone: str):
    funcionario = Funcionario(nome=nome, cargo=cargo, especialidade=especialidade, crm=crm, telefone=telefone)
    db.add(funcionario)
    db.commit()
    db.refresh(funcionario)
    return funcionario


def create_consulta(db: Session, id_paciente: int, id_funcionario: int, data_hora):
    consulta = Consulta(id_paciente=id_paciente, id_funcionario=id_funcionario, data_hora=data_hora)
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta


def create_internacao(db: Session, id_paciente: int, id_leito: int, data_entrada, data_saida=None):
    internacao = Internacao(id_paciente=id_paciente, id_leito=id_leito, data_entrada=data_entrada, data_saida=data_saida)
    db.add(internacao)

    # Trigger: marcar leito como indisponível
    marcar_leito_indisponivel(db, id_leito)

    db.commit()
    db.refresh(internacao)
    return internacao


def create_leito(db: Session, numero: str, tipo: str, disponivel: bool = True):
    leito = Leito(numero=numero, tipo=tipo, disponivel=disponivel)
    db.add(leito)
    db.commit()
    db.refresh(leito)
    return leito


def create_exame(db: Session, id_paciente: int, id_funcionario: int, tipo: str, resultado: str, data):
    exame = Exame(tipo=tipo, resultado=resultado, data=data, id_paciente=id_paciente, id_funcionario=id_funcionario)
    db.add(exame)
    db.commit()
    db.refresh(exame)
    return exame


def create_agendamento(db: Session, id_paciente: int, id_funcionario: int, data_hora, tipo: str):
    agendamento = Agendamento(data_hora=data_hora, tipo=tipo, paciente_id=id_paciente, funcionario_id=id_funcionario)
    db.add(agendamento)

    # Trigger: gerar fatura automática
    gerar_fatura_automatica(db, id_paciente, id_funcionario)

    db.commit()
    db.refresh(agendamento)
    return agendamento

def create_fatura(db: Session, id_paciente: int, id_funcionario: int, data_emissao, valor: float, status_pag: str):
    fatura = Fatura(data_emissao=data_emissao, valor=valor, status_pag=status_pag, paciente_id=id_paciente, funcionario_id=id_funcionario)
    db.add(fatura)
    db.commit()
    db.refresh(fatura)
    return fatura


def create_prescricao(db: Session, id_paciente: int, id_funcionario: int, data_prescricao):
    prescricao = Prescricao(data_prescricao=data_prescricao, paciente_id=id_paciente, funcionario_id=id_funcionario)
    db.add(prescricao)
    db.commit()
    db.refresh(prescricao)
    return prescricao


def add_medicamento_prescricao(db: Session, id_prescricao: int, id_medicamento: int, quantidade: int, instrucoes: str):
    assoc = PrescricaoMedicamento(id_prescricao=id_prescricao, id_medicamento=id_medicamento, quantidade=quantidade, instrucoes=instrucoes)
    db.add(assoc)
    db.commit()
    db.refresh(assoc)
    return assoc
