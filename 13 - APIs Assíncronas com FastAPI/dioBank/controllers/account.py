from typing import Annotated

from fastapi import APIRouter, Cookie, Header, HTTPException, Response, status

from schemas.account import ContaCreate, ContaResponse, StatusConta
from services.account import AccountService

router = APIRouter(prefix="/contas", tags=["Contas"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ContaResponse)
def create_conta(conta: ContaCreate):
    return AccountService.criar_conta(conta)


@router.get("/", response_model=list[ContaResponse])
def read_contas(
    response: Response,
    status_filtro: StatusConta,
    limit: int,
    skip: int = 0,
    session_id: Annotated[str | None, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
):
    response.set_cookie(key="session_id", value="sarah@gmail.com")
    print(f"Cookie: {session_id}")
    print(f"User-Agent: {user_agent}")

    return AccountService.listar_contas(
        status_filtro=status_filtro,
        skip=skip,
        limit=limit,
    )


@router.get("/{numero_conta}", response_model=ContaResponse)
def consultar_conta(numero_conta: int):
    conta = AccountService.buscar_conta(numero_conta)

    if conta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada")

    return conta
