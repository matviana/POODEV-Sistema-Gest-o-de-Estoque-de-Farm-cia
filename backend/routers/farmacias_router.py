from fastapi import APIRouter, HTTPException
from backend.database import (
    cadastrar_farmacia,
    listar_farmacias,
    buscar_farmacia_por_id,
    atualizar_farmacia,
    deletar_farmacia
)

router = APIRouter(prefix="/farmacias", tags=["Farmácias"])



# CADASTRAR FARMÁCIA

@router.post("/")
def cadastrar(nome: str, endereco: str, telefone: str, cnpj: str):
    nova_id = cadastrar_farmacia(nome, endereco, telefone, cnpj)

    if nova_id is None:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar farmácia.")

    return {"status": "ok", "id": nova_id}



# LISTAR TODAS

@router.get("/")
def listar():
    dados = listar_farmacias()

    resultados = [
        {
            "id": d[0],
            "nome": d[1],
            "endereco": d[2],
            "telefone": d[3],
            "cnpj": d[4]
        }
        for d in dados
    ]

    return {"total": len(resultados), "farmacias": resultados}



# BUSCAR POR ID

@router.get("/{id_farmacia}")
def buscar(id_farmacia: int):
    dado = buscar_farmacia_por_id(id_farmacia)

    if dado is None:
        raise HTTPException(status_code=404, detail="Farmácia não encontrada.")

    return {
        "id": dado[0],
        "nome": dado[1],
        "endereco": dado[2],
        "telefone": dado[3],
        "cnpj": dado[4],
    }



# ATUALIZAR FARMÁCIA

@router.put("/{id_farmacia}")
def atualizar(id_farmacia: int, nome: str, endereco: str, telefone: str):
    ok = atualizar_farmacia(id_farmacia, nome, endereco, telefone)

    if not ok:
        raise HTTPException(status_code=400, detail="Erro ao atualizar.")

    return {"status": "ok", "mensagem": "Farmácia atualizada com sucesso."}



# DELETAR

@router.delete("/{id_farmacia}")
def deletar(id_farmacia: int):
    ok = deletar_farmacia(id_farmacia)

    if not ok:
        raise HTTPException(status_code=404, detail="Farmácia não encontrada ou não deletada.")

    return {"status": "ok", "mensagem": "Farmácia removida com sucesso."}
