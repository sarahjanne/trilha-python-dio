from typing import Annotated

from fastapi import APIRouter, Cookie, Header, HTTPException, Response, status

from schemas.account import ContaCreate, ContaResponse, StatusConta, OperacaoFinanceira
from services.account import AccountService

# O prefixo e a tag já organizam tudo no Swagger!
router = APIRouter(prefix="/contas", tags=["Contas"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ContaResponse, summary="Criar uma nova conta")
def create_conta(conta: ContaCreate):
    """
    Cria uma nova conta bancária no sistema.
    
    O número da conta é gerado automaticamente pela API.
    O status inicial padrão é sempre **ativa**.
    """
    return AccountService.criar_conta(conta)


@router.get("/", response_model=list[ContaResponse], summary="Listar contas bancárias")
def read_contas(
    response: Response,
    status_filtro: StatusConta,
    limit: int,
    skip: int = 0,
    session_id: Annotated[str | None, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
):
    """
    Retorna uma lista de contas com base no status.
    
    **Filtros suportados:**
    - `status_filtro`: Obrigatório. Filtra por ativa, encerrada, etc.
    - `limit`: Quantidade máxima de contas retornadas.
    - `skip`: Quantidade de registros para pular (paginação).
    
    *Nota: Esta rota também injeta um cookie de sessão.*
    """

    response.set_cookie(key="session_id", value="sarah@falabella.com")
    print(f"Cookie: {session_id}")
    print(f"User-Agent: {user_agent}")

    return AccountService.listar_contas(
        status_filtro=status_filtro,
        skip=skip,
        limit=limit,
    )


@router.get("/{numero_conta}", response_model=ContaResponse, summary="Consultar saldo e dados da conta")
def consultar_conta(numero_conta: int):

    """
    Busca os detalhes de uma conta específica usando o seu número identificador.
    
    Retorna o erro **404 Not Found** caso a conta não exista no banco de dados.
    """
    
    conta = AccountService.buscar_conta(numero_conta)

    if conta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada")

    return conta

@router.post(
    "/{numero_conta}/deposito", 
    response_model=ContaResponse,
    summary="Realizar um depósito"
)
def realizar_deposito(numero_conta: int, operacao: OperacaoFinanceira):
    """
    Adiciona saldo a uma conta existente. O valor deve ser maior que zero.
    """
    conta = AccountService.depositar(numero_conta, operacao)
    
    if not conta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada")
        
    return conta


@router.post(
    "/{numero_conta}/saque", 
    response_model=ContaResponse,
    summary="Realizar um saque"
)
def realizar_saque(numero_conta: int, operacao: OperacaoFinanceira):
    """
    Subtrai saldo de uma conta existente. 
    Retorna erro 400 caso o valor solicitado seja maior que o saldo disponível.
    """
    resultado = AccountService.sacar(numero_conta, operacao)
    
    if resultado is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada")
        
    if resultado == "saldo_insuficiente":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Saldo insuficiente para esta operação")
        
    return resultado