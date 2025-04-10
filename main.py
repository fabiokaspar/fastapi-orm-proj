from fastapi import FastAPI
import models.models as models
import uvicorn
from config.database import engine
from routers.cliente import router as cliente_router
from routers.produto import router as produto_router
from routers.contrato import router as contrato_router

openapi_tags = [
    {
        "name": "Cliente",
        "description": "Gerenciamento de clientes."
    },
    {
        "name": "Produto",
        "description": "Gerenciamento de produtos."
    },
    {
        "name": "Contrato",
        "description": "Gerenciamento de contratos de previdência."
    }
]


app = FastAPI(description="API de Previdência Privada",
              openapi_tags=openapi_tags, 
              version="1.0.0")


models.Base.metadata.create_all(bind=engine)

app.include_router(cliente_router)
app.include_router(produto_router)
app.include_router(contrato_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8000,
        reload=True
    )
