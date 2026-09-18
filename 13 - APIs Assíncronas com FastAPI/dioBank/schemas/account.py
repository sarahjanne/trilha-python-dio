from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field


class StatusConta(str, Enum):
    ATIVA = "ativa"
    ENCERRADA = "encerrada"
    BLOQUEADA = "bloqueada"
    PENDENTE = "pendente"

class ContaCreate(BaseModel):
    titular: str = Field(..., examples=["Joana Prado"])
    saldo_inicial: float = Field(default=0.0, ge=0, examples=[1500.50])
    data_abertura: datetime = Field(default_factory=lambda: datetime.now(UTC))
    status: StatusConta = Field(default=StatusConta.ATIVA, examples=[StatusConta.ATIVA])

class ContaResponse(BaseModel):
    numero_conta: int
    titular: str
    saldo_inicial: float
    data_abertura: datetime
    status: StatusConta

class OperacaoFinanceira(BaseModel):
    valor: float = Field(..., gt=0, description="Valor da transação", examples=[50.0])