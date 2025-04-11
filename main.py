from fastapi import FastAPI
import models.models as models
import uvicorn
from config.database import engine
from routers.cliente import router as cliente_router
from routers.produto import router as produto_router

openapi_tags = [
    {
        "name": "Cliente",
        "description": "Gerenciamento de clientes."
    },
    {
        "name": "Produto",
        "description": "Gerenciamento de produtos."
    }
]


app = FastAPI(description="API Prev",
              openapi_tags=openapi_tags, 
              version="1.0.0")


models.Base.metadata.create_all(bind=engine)

app.include_router(cliente_router)
app.include_router(produto_router)

if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(
        "main:app",
        port=8000,
        reload=True
    )
