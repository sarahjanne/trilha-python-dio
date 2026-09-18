from fastapi import FastAPI

from controllers.account import router as account_router

app = FastAPI(
    title="Banco Falabella",
    description="API para gerenciamento de contas bancárias e clientes do projeto de estudos.",
    version="1.0.0",
    contact={
        "name": "Banco Falabella",
        "email": "atendimento@falabella.com",
    }
)

app.include_router(account_router)


@app.get("/", tags=["Healthcheck"], summary="Verifica a saúde da API")
def healthcheck():
    # O return continua igual. É apenas a resposta do endpoint.
    return {"message": "API do banco funcionando"}
