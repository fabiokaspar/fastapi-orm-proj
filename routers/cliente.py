from http.client import HTTPResponse
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import models.models as models
from fastapi.responses import JSONResponse
from config.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter(prefix='/api/clientes', tags=['Cliente'])

class Cliente(BaseModel):
    cpf: str
    nome: str
    email: EmailStr
    dataNascimento: datetime
    genero: str
    rendaMensal: float

@router.get('')
async def get_clientes(db: Session=Depends(get_db)):
    try:
        result = db.query(models.Cliente).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Not Found")
    return result

@router.get('/{cliente_id}')
async def get_cliente_by_id(cliente_id: int, db: Session=Depends(get_db)):
    try:
        result = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Not Found")
    return result

@router.post("")
async def create_cliente(cliente: Cliente, db: Session=Depends(get_db)):
    db_client = models.Cliente(**cliente.dict())
    try:
        db.add(db_client)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Cliente cadastrado com sucesso", "id": db_client.id}) 
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro ao cadastrar cliente")
