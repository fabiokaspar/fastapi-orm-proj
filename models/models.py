from sqlalchemy import Column, Integer, DateTime, Float, String
from config.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cpf = Column(String, index=True, unique=True)
    nome = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    dataNascimento = Column(DateTime)
    genero = Column(String)
    rendaMensal = Column(Float)

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, index=True)
    susep = Column(String)
    expiracaoVenda = Column(DateTime)
    valorMinimoAporteInicial = Column(Float)
    valorMinimoAporteExtra = Column(Float)
    idadeEntrada = Column(Integer)
    idadeSaida = Column(Integer)
