from datetime import UTC, datetime

from schemas.account import ContaCreate, StatusConta


fake_contas_db = [
    {
        "numero_conta": 1001,
        "titular": "Maria Silva",
        "saldo_inicial": 2500.75,
        "data_abertura": datetime.now(UTC),
        "status": StatusConta.ATIVA,
    },
    {
        "numero_conta": 1002,
        "titular": "João Pedro",
        "saldo_inicial": 150.00,
        "data_abertura": datetime.now(UTC),
        "status": StatusConta.ATIVA,
    },
    {
        "numero_conta": 1003,
        "titular": "Ana Clara",
        "saldo_inicial": 8900.50,
        "data_abertura": datetime.now(UTC),
        "status": StatusConta.ENCERRADA,
    },
]


class AccountService:
    @staticmethod
    def criar_conta(conta: ContaCreate):
        numero_conta = max((c["numero_conta"] for c in fake_contas_db), default=1000) + 1

        nova_conta = {
            "numero_conta": numero_conta,
            **conta.model_dump(),
        }

        fake_contas_db.append(nova_conta)
        return nova_conta

    @staticmethod
    def listar_contas(status_filtro: StatusConta, skip: int = 0, limit: int = 10):
        contas = [conta for conta in fake_contas_db if conta["status"] == status_filtro]
        return contas[skip : skip + limit]

    @staticmethod
    def buscar_conta(numero_conta: int):
        for conta in fake_contas_db:
            if conta["numero_conta"] == numero_conta:
                return conta
        return None
