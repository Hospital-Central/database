from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from database.setup import Base

class Paciente(Base):
    __tablename__ = 'paciente'
    id = Column('ID_Paciente', Integer, primary_key=True)
    nome = Column(String)
    data_nascimento = Column(Date)
    cpf = Column(String)
    telefone = Column(String)
    endereco = Column(String)

    consultas = relationship('Consulta', back_populates='paciente')
    internacoes = relationship('Internacao', back_populates='paciente')
    exames = relationship('Exame', back_populates='paciente')
    agendamentos = relationship('Agendamento', back_populates='paciente')
    prescricoes = relationship('Prescricao', back_populates='paciente')
    faturas = relationship('Fatura', back_populates='paciente')

class Funcionario(Base):
    __tablename__ = 'funcionario'
    id = Column('ID_Funcionario', Integer, primary_key=True)
    nome = Column(String)
    cargo = Column(String)
    especialidade = Column(String)
    crm = Column(String)
    telefone = Column(String)

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
    numero = Column(String)
    tipo = Column(String)
    disponivel = Column(Boolean)

    internacoes = relationship('Internacao', back_populates='leito')