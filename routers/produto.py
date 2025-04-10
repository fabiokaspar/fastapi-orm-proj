from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import models.models as models
from fastapi.responses import JSONResponse
from config.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter(prefix='/api/produtos', tags=['Produto'])

class Produto(BaseModel):
    nome: str
    susep: str 
    expiracaoVenda: datetime
    valorMinimoAporteInicial: float
    valorMinimoAporteExtra: float
    idadeEntrada: int
    idadeSaida: int

@router.get('')
async def get_produtos(db: Session=Depends(get_db)):
    try:
        result = db.query(models.Produto).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Not Found")
    return result

@router.get('/{produto_id}')
async def get_produto_by_id(produto_id: int, db: Session=Depends(get_db)):
    try:
        result = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Not Found")
    return result

@router.post("")
async def create_produto(produto: Produto, db: Session=Depends(get_db)):
    db_product = models.Produto(**produto.dict())
    try:
        db.add(db_product)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Produto cadastrado com sucesso", "id": db_product.id}) 
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro ao cadastrar produto")
