from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from database.setup import Base

class Paciente(Base):
    __tablename__ = 'paciente'
    id = Column('ID_Paciente', Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    data_nascimento = Column(Date)
    cpf = Column(String(14), unique=True)
    telefone = Column(String(20))
    endereco = Column(String(255))
    ativo = Column(Boolean, default=True)

    consultas = relationship('Consulta', back_populates='paciente')
    internacoes = relationship('Internacao', back_populates='paciente')
    exames = relationship('Exame', back_populates='paciente')
    agendamentos = relationship('Agendamento', back_populates='paciente')
    prescricoes = relationship('Prescricao', back_populates='paciente')
    faturas = relationship('Fatura', back_populates='paciente')

class Funcionario(Base):
    __tablename__ = 'funcionario'
    id = Column('ID_Funcionario', Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cargo = Column(String(50))
    especialidade = Column(String(50))
    crm = Column(String(20), unique=True)
    telefone = Column(String(20))

    consultas = relationship('Consulta', back_populates='funcionario')
    exames = relationship('Exame', back_populates='funcionario')
    prescricoes = relationship('Prescricao', back_populates='funcionario')
    agendamentos = relationship('Agendamento', back_populates='funcionario')
    faturas = relationship('Fatura', back_populates='funcionario')

class Consulta(Base):
    __tablename__ = 'consulta'
    id = Column('ID_Consulta', Integer, primary_key=True)
    data_hora = Column(DateTime)
    id_paciente = Column(Integer, ForeignKey('paciente.ID_Paciente'))
    id_funcionario = Column(Integer, ForeignKey('funcionario.ID_Funcionario'))

    paciente = relationship('Paciente', back_populates='consultas')
    funcionario = relationship('Funcionario', back_populates='consultas')

class Internacao(Base):
    __tablename__ = 'internacao'
    id = Column('ID_Internacao', Integer, primary_key=True)
    data_entrada = Column(DateTime)
    data_saida = Column(DateTime)
    id_paciente = Column(Integer, ForeignKey('paciente.ID_Paciente'))
    id_leito = Column(Integer, ForeignKey('leito.ID_Leito'))

    paciente = relationship('Paciente', back_populates='internacoes')
    leito = relationship('Leito', back_populates='internacoes')

class Leito(Base):
    __tablename__ = 'leito'
    id = Column('ID_Leito', Integer, primary_key=True)
    numero = Column(String(10))
    tipo = Column(String(50))
    disponivel = Column(Boolean)

    internacoes = relationship('Internacao', back_populates='leito')

class Exame(Base):
    __tablename__='exame'
    id = Column('ID_Exame', Integer, primary_key=True)
    tipo = Column(String(50))
    resultado = Column(String(255))
    data = Column(DateTime)

    id_paciente = Column(Integer, ForeignKey('paciente.ID_Paciente'))
    id_funcionario = Column(Integer, ForeignKey('funcionario.ID_Funcionario'))


    paciente = relationship('Paciente', back_populates='exames')
    funcionario = relationship('Funcionario', back_populates='exames')

class Agendamento(Base):
    __tablename__ = 'agendamento'
    id = Column('ID_Agendamento', Integer, primary_key=True)
    data_hora = Column(DateTime)
    tipo = Column(String(50))
    paciente_id = Column(Integer, ForeignKey('paciente.ID_Paciente'))
    funcionario_id = Column(Integer, ForeignKey('funcionario.ID_Funcionario'))

    paciente = relationship('Paciente', back_populates='agendamentos')
    funcionario = relationship('Funcionario', back_populates='agendamentos')

class Fatura(Base):
    __tablename__ = 'fatura'
    id = Column('ID_Fatura', Integer, primary_key=True)
    data_emissao = Column(DateTime)
    valor = Column(Float)
    status_pag = Column(String(50))

    paciente_id = Column(Integer, ForeignKey('paciente.ID_Paciente'))
    funcionario_id = Column(Integer, ForeignKey('funcionario.ID_Funcionario'))


    paciente = relationship('Paciente', back_populates='faturas')
    funcionario = relationship('Funcionario', back_populates='faturas')

class Prescricao(Base):
    __tablename__ = 'prescricao'
    id = Column('ID_Prescricao', Integer, primary_key=True)
    data_prescricao = Column(DateTime)
    paciente_id = Column(Integer, ForeignKey('paciente.ID_Paciente'))
    funcionario_id = Column(Integer, ForeignKey('funcionario.ID_Funcionario'))

    paciente = relationship('Paciente', back_populates='prescricoes')
    funcionario = relationship('Funcionario', back_populates='prescricoes')
    medicamentos_assoc = relationship("PrescricaoMedicamento", back_populates="prescricao")


class Medicamento(Base):
    __tablename__ = 'medicamento'
    id = Column('ID_Medicamento', Integer, primary_key=True)
    nome_med = Column(String(100)) 
    dosagem = Column(String(50))
    frequencia = Column(String(50))

    prescricoes_assoc = relationship("PrescricaoMedicamento", back_populates="medicamento")

class PrescricaoMedicamento(Base):
    __tablename__ = 'prescricao_medicamento'
    id_prescricao = Column(Integer, ForeignKey('prescricao.ID_Prescricao'), primary_key=True)
    id_medicamento = Column(Integer, ForeignKey('medicamento.ID_Medicamento'), primary_key=True)
    quantidade = Column(Integer)
    instrucoes = Column(String(255))

    prescricao = relationship("Prescricao", back_populates="medicamentos_assoc")
    medicamento = relationship("Medicamento", back_populates="prescricoes_assoc")

