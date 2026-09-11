from enum import Enum

from datetime import UTC, datetime

from fastapi import FastAPI, status 
from pydantic import BaseModel

app = FastAPI()

# Definindo os status permitidos no seu banco
class StatusConta(str, Enum):
    ATIVA = "ativa"
    ENCERRADA = "encerrada"
    BLOQUEADA = "bloqueada"
    PENDENTE = "pendente"

#Lista simulando o banco de dados de contas bancárias

fake_contas_db = [
    {"numero_conta": 1001, "titular": "Maria Silva", "saldo_disponivel": 2500.75, "data_consulta": datetime.now(UTC), "status": StatusConta.ATIVA},
    {"numero_conta": 1002, "titular": "João Pedro", "saldo_disponivel": 150.00, "data_consulta": datetime.now(UTC), "status": StatusConta.ATIVA},
    {"numero_conta": 1003, "titular": "Ana Clara", "saldo_disponivel": 8900.50, "data_consulta": datetime.now(UTC), "status": StatusConta.ENCERRADA},
    {"numero_conta": 1004, "titular": "Carlos Eduardo", "saldo_disponivel": -50.20, "data_consulta": datetime.now(UTC), "status": StatusConta.ATIVA},
    {"numero_conta": 1005, "titular": "Beatriz Souza", "saldo_disponivel": 12000.00, "data_consulta": datetime.now(UTC), "status": StatusConta.BLOQUEADA},
]

class Conta(BaseModel):
    titular: str
    saldo_inicial: float = 0.0 # Define 0.0 como padrão se a pessoa não depositar nada ao abrir
    data_abertura: datetime = datetime.now(UTC)
    status: StatusConta = StatusConta.ATIVA

@app.post("/contas/" ,status_code=status.HTTP_201_CREATED)
def create_conta(conta: Conta):
   fake_contas_db.append(conta.model_dump())
   return conta

@app.get("/contas/")
def read_contas(status: StatusConta, limit: int, skip: int = 0):  #Aqui o 'limit' é obrigatório, e o 'skip' é opcional, com valor padrão de 0
    #def listar_contas(skip: int = 0, limit: int = len(fake_contas_db), status: StatusConta = StatusConta): -> Limita a lista em até 4 elementos
    #return [conta for conta in fake_contas_db[skip: skip + limit] if conta["status"] == status] -> O 'skip' é usado para pular os primeiros elementos da lista, e o 'limit' é usado para limitar a quantidade de elementos retornados. O filtro 'if conta["status"] == status' garante que apenas as contas com o status especificado sejam retornadas.
    contas = []
    # Filtra por status e já aplica o skip e limit matematicamente
    return [conta for conta in fake_contas_db if conta["status"] == status][skip: skip + limit]


"""
fake_contas_db = [
    {"numero_conta": 1001, "titular": "Maria Silva", "saldo_disponivel": 2500.75, "data_consulta": datetime.now(UTC), "ativa": True},
    {"numero_conta": 1002, "titular": "João Pedro", "saldo_disponivel": 150.00, "data_consulta": datetime.now(UTC), "ativa": True},
    {"numero_conta": 1003, "titular": "Ana Clara", "saldo_disponivel": 8900.50, "data_consulta": datetime.now(UTC), "ativa": False}, # Conta encerrada
    {"numero_conta": 1004, "titular": "Carlos Eduardo", "saldo_disponivel": -50.20, "data_consulta": datetime.now(UTC), "ativa": True},
    {"numero_conta": 1005, "titular": "Beatriz Souza", "saldo_disponivel": 12000.00, "data_consulta": datetime.now(UTC), "ativa": True},
]

@app.get("/contas")
def listar_contas(skip: int = 0, limit: int = len(fake_contas_db), ativa: bool = True):
    return [conta for conta in fake_contas_db[skip: skip + limit] if conta["ativa"] is ativa]
"""
# Endpoint para consultar informações de uma conta bancária
@app.get("/contas/{numero_conta}")
def consultar_conta(numero_conta: int):
    return {
        "banco": "Banco FastAPI",
        "agencia": "0001",
        "numero_conta": numero_conta,
        "titular": "Maria Silva",
        "saldo_disponivel": 2500.75,
        "moeda": "BRL",
        "data_consulta": datetime.now(UTC)
    }