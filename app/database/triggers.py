import datetime
from sqlalchemy.orm import Session
from database.models import (
    Paciente, Funcionario, Consulta, Internacao, Leito,
    Exame, Agendamento, Fatura, Prescricao, Medicamento, PrescricaoMedicamento
)


def marcar_leito_indisponivel(db: Session, id_leito: int):
    leito = db.query(Leito).filter(Leito.id == id_leito).first()
    if leito:
        leito.disponivel = False
       

def gerar_fatura_automatica(db: Session, id_paciente: int, id_funcionario: int):
    fatura = Fatura(
        data_emissao=datetime.datetime.now(),
        valor=100.0,  
        status_pag="Pendente",
        id_paciente=id_paciente,
        id_funcionario=id_funcionario
    )
    db.add(fatura)
  


def create_internacao(db: Session, id_paciente: int, id_leito: int, data_entrada, data_saida=None):
    internacao = Internacao(
        id_paciente=id_paciente,
        id_leito=id_leito,
        data_entrada=data_entrada,
        data_saida=data_saida
    )
    db.add(internacao)

    marcar_leito_indisponivel(db, id_leito)

    db.commit()
    db.refresh(internacao)
    return internacao


def dar_alta(db: Session, internacao_id: int, nova_data_saida):
    internacao = db.query(Internacao).filter(Internacao.id == internacao_id).first()
    if not internacao:
        raise ValueError("Internação não encontrada.")
    if internacao.data_saida is not None:
        raise ValueError("Internação já tem data de saída.")

    internacao.data_saida = nova_data_saida

    leito = db.query(Leito).filter(Leito.id == internacao.id_leito).first()
    if leito:
        leito.disponivel = True

    db.commit()
    db.refresh(internacao)
    return internacao


def create_agendamento(db: Session, id_paciente: int, id_funcionario: int, data_hora, tipo: str):
    agendamento = Agendamento(
        data_hora=data_hora,
        tipo=tipo,
        id_paciente=id_paciente,
        id_funcionario=id_funcionario
    )
    db.add(agendamento)

    gerar_fatura_automatica(db, id_paciente, id_funcionario)

    db.commit()
    db.refresh(agendamento)
    return agendamento


def cancelar_agendamento(db: Session, agendamento_id: int):
    agendamento = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if not agendamento:
        return None

    fatura = db.query(Fatura).filter(
        Fatura.id_paciente == agendamento.id_paciente,
        Fatura.id_funcionario == agendamento.id_funcionario,
        Fatura.status_pag == 'Pendente'
    ).order_by(Fatura.data_emissao.desc()).first()

    db.delete(agendamento)

    if fatura:
        fatura.status_pag = "Cancelada"

    db.commit()
    return True


def desativar_paciente(db: Session, paciente_id: int):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if paciente:
        paciente.ativo = False
        db.commit()
        return paciente
    return None


def create_prescricao_com_validacao(db: Session, id_paciente: int, id_funcionario: int, data_prescricao, medicamentos: list):
    if not medicamentos:
        raise ValueError("A prescrição deve conter pelo menos um medicamento.")

    prescricao = Prescricao(
        data_prescricao=data_prescricao,
        id_paciente=id_paciente,
        id_funcionario=id_funcionario
    )
    db.add(prescricao)
    db.commit()
    db.refresh(prescricao)

    for med in medicamentos:
        assoc = PrescricaoMedicamento(
            id_prescricao=prescricao.id,
            id_medicamento=med['id_medicamento'],
            quantidade=med['quantidade'],
            instrucoes=med['instrucoes']
        )
        db.add(assoc)

    db.commit()
    return prescricao

