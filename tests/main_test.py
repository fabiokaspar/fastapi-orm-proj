from datetime import datetime
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# teste de unidade garante que seja possível cadastrar um cliente com os campos obrigatórios
def test_create_client_success():
    payload = {
        "cpf": "12345678",
        "nome": "Fulano de Tal",
        "email": "fulanodetal@email.com",
        "dataNascimento": "2010-04-08T17:44:10.218Z",
        "genero": "masculino",
        "rendaMensal": 100
    }
    response = client.post("/api/clientes", json=payload)

    assert response.status_code == 201
    data = response.json()
    
    assert "id" in data
    assert isinstance(data["id"], int)


def test_create_client_fail():
    payload = {
        "cpf": "123444",
        "nome": "Fulano de Tal",
        "email": "emailinvalido.com",
        "dataNascimento": "2010-04-08T17:44:10.218Z",
        "genero": "masculino",
        "rendaMensal": 100
    }
    response = client.post("/api/clientes", json=payload)

    assert response.status_code == 422
