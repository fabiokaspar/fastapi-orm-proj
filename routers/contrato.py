from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import models.models as models
from fastapi.responses import JSONResponse
from config.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter(prefix='/api/contratos', tags=['Contrato'])

class Contrato(BaseModel):
    idCliente: int
    idProduto: int
    aporte: float
    aporteExtra: float = 0.0
    dataContratacao: datetime = datetime.now()

@router.get('')
async def get_contrato(db: Session=Depends(get_db)):
    try:
        result = db.query(models.Contrato).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Not Found")
    return result

@router.get('/{contrato_id}')
async def get_contrato_by_id(contrato_id: int, db: Session=Depends(get_db)):
    try:
        result = db.query(models.Contrato).filter(models.Contrato.id == contrato_id).first()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Not Found")
    return result

@router.post("")
async def create_contrato(contrato: Contrato, db: Session=Depends(get_db)):
    db_contrato = models.Contrato(**contrato.dict())

    idCliente = contrato.idCliente
    cliente = db.query(models.Cliente).filter(models.Cliente.id == idCliente).first()
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    idProduto = contrato.idProduto
    produto = db.query(models.Produto).filter(models.Produto.id == idProduto).first()
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # verifica se produto não está expirado
    if produto.expiracaoVenda < datetime.now():
        raise HTTPException(status_code=400, detail="Produto expirado")
    
    # verifica se o aporte inicial é maior que o mínimo permitido
    if contrato.aporte < produto.valorMinimoAporteInicial:
        raise HTTPException(status_code=400, detail="Aporte menor que o mínimo permitido")
    
    # verifica se o aporte extra é maior que o mínimo permitido
    if contrato.aporteExtra < produto.valorMinimoAporteExtra:
        raise HTTPException(status_code=400, detail="Aporte extra menor que o mínimo permitido")
   
    idadeAposentadoria = contrato.dataContratacao.year - cliente.dataNascimento.year

    # idadeAposentadoria deve ser maior que idadeEntrada e menor que idadeSaida do produto
    if idadeAposentadoria > produto.idadeSaida or idadeAposentadoria < produto.idadeEntrada:
        raise HTTPException(status_code=400, detail="Idade de aposentadoria fora do intervalo permitido")
    
    try:
        db.add(db_contrato)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Contrato cadastrado com sucesso", "id": db_contrato.id}) 
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro ao cadastrar contrato")
