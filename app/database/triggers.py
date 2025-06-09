import datetime
from sqlalchemy.orm import Session
from database.models import (
    Paciente, Funcionario, Consulta, Internacao, Leito,
    Exame, Agendamento, Fatura, Prescricao, Medicamento, PrescricaoMedicamento
)

# 1. Criar internação e atualizar leito para indisponível
def create_internacao(db: Session, id_paciente: int, id_leito: int, data_entrada, data_saida=None):
    internacao = Internacao(
        id_paciente=id_paciente,
        id_leito=id_leito,
        data_entrada=data_entrada,
        data_saida=data_saida
    )
    db.add(internacao)

    # Trigger simulada: atualizar leito para indisponível
    leito = db.query(Leito).filter(Leito.id == id_leito).first()
    if leito:
        leito.disponivel = False

    db.commit()
    db.refresh(internacao)
    return internacao


# 2. Dar alta na internação e liberar leito
def dar_alta(db: Session, id_internacao: int, nova_data_saida):
    internacao = db.query(Internacao).filter(Internacao.id == id_internacao).first()
    if internacao and internacao.data_saida is None and nova_data_saida:
        internacao.data_saida = nova_data_saida

        leito = db.query(Leito).filter(Leito.id == internacao.id_leito).first()
        if leito:
            leito.disponivel = True

        db.commit()
        db.refresh(internacao)
        return internacao
    return None


# 3. Criar agendamento e gerar fatura automaticamente
def create_agendamento(db: Session, id_paciente: int, id_funcionario: int, data_hora, tipo: str):
    agendamento = Agendamento(
        data_hora=data_hora,
        tipo=tipo,
        paciente_id=id_paciente,
        funcionario_id=id_funcionario
    )
    db.add(agendamento)

    # Trigger simulada: criar fatura associada
    fatura = Fatura(
        data_emissao=datetime.datetime.now(),
        valor=100.00,  # valor fixo como exemplo
        status_pag="Pendente",
        paciente_id=id_paciente,
        funcionario_id=id_funcionario
    )
    db.add(fatura)

    db.commit()
    db.refresh(agendamento)
    return agendamento


# 4. Cancelar agendamento e cancelar fatura pendente relacionada
def cancelar_agendamento(db: Session, id_agendamento: int):
    agendamento = db.query(Agendamento).filter(Agendamento.id == id_agendamento).first()
    if not agendamento:
        return None

    # Buscar fatura pendente mais recente relacionada ao paciente e funcionário
    fatura = db.query(Fatura).filter(
        Fatura.paciente_id == agendamento.paciente_id,
        Fatura.funcionario_id == agendamento.funcionario_id,
        Fatura.status_pag == 'Pendente'
    ).order_by(Fatura.data_emissao.desc()).first()

    db.delete(agendamento)

    if fatura:
        fatura.status_pag = "Cancelada"

    db.commit()
    return True


# 5. Marcar paciente como inativo ao invés de deletar
def desativar_paciente(db: Session, id_paciente: int):
    paciente = db.query(Paciente).filter(Paciente.id == id_paciente).first()
    if paciente:
        paciente.ativo = False  # Certifique-se que o campo 'ativo' existe no model Paciente
        db.commit()
        return paciente
    return None


# 6. Criar prescrição e exigir que pelo menos um medicamento seja associado
def create_prescricao_com_validacao(db: Session, id_paciente: int, id_funcionario: int, data_prescricao, medicamentos: list):
    if not medicamentos:
        raise ValueError("A prescrição deve conter pelo menos um medicamento.")

    prescricao = Prescricao(
        data_prescricao=data_prescricao,
        paciente_id=id_paciente,
        funcionario_id=id_funcionario
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
