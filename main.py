from fastapi import FastAPI
import models.models as models
import uvicorn
from config.database import engine
from routers.cliente import router as cliente_router
from routers.produto import router as produto_router
from fastapi.responses import JSONResponse

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


@app.get("/", tags=["Health Check"])
async def health_check():
    return JSONResponse(status_code=200, content={"status": "ok - API is running"})


app.include_router(cliente_router)
app.include_router(produto_router)
