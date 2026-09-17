from fastapi import FastAPI

from controllers.account import router as account_router

app = FastAPI(title="Banco FastAPI")

app.include_router(account_router)


@app.get("/")
def healthcheck():
    return {"message": "API do banco funcionando"}
