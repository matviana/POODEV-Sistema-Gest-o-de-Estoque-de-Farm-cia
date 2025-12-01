from fastapi import APIRouter, HTTPException
from backend.schemas.medicamentos_schema import (
    MedicamentoCreate,
    MedicamentoUpdate,
    MedicamentoResponse,
)
from backend.database import get_db_connection
from datetime import date, timedelta
from fastapi import Query

router = APIRouter(prefix="/medicamentos", tags=["Medicamentos"])



#   LISTAR TODOS

@router.get("/", response_model=list[MedicamentoResponse])
def listar_medicamentos():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, nome, lote, validade, quantidade_minima, codigo_barras,
               quantidade_estoque, receita_obrigatoria
        FROM medicamentos;
    """)

    rows = cur.fetchall()
    conn.close()

    medicamentos = []
    for row in rows:
        medicamentos.append({
            "id": row[0],
            "nome": row[1],
            "lote": row[2],
            "validade": row[3],
            "quantidade_minima": row[4],
            "codigo_barras": row[5],
            "quantidade_estoque": row[6],
            "receita_obrigatoria": row[7],
        })

    return medicamentos


#   ALERTAS DE VENCIMENTO
@router.get("/alertas_vencimento", response_model=list[MedicamentoResponse])
def alertas_vencimento(dias_aviso: int = Query(30, description="Número de dias antes do vencimento para alertar")):
    """
    Retorna os medicamentos que estão vencendo em até `dias_aviso` dias ou já estão vencidos.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    hoje = date.today()
    limite = hoje + timedelta(days=dias_aviso)

    cur.execute("""
        SELECT id, nome, lote, validade, quantidade_minima, codigo_barras,
               quantidade_estoque, receita_obrigatoria
        FROM medicamentos
        WHERE validade <= %s
        ORDER BY validade ASC;
    """, (limite,))

    rows = cur.fetchall()
    conn.close()

    medicamentos = []
    for row in rows:
        medicamentos.append({
            "id": row[0],
            "nome": row[1],
            "lote": row[2],
            "validade": row[3],
            "quantidade_minima": row[4],
            "codigo_barras": row[5],
            "quantidade_estoque": row[6],
            "receita_obrigatoria": row[7],
        })

    return medicamentos



@router.get("/{id}", response_model=MedicamentoResponse)
def buscar_medicamento(id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, nome, lote, validade, quantidade_minima, codigo_barras,
               quantidade_estoque, receita_obrigatoria
        FROM medicamentos WHERE id = %s;
    """, (id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")

    return {
        "id": row[0],
        "nome": row[1],
        "lote": row[2],
        "validade": row[3],
        "quantidade_minima": row[4],
        "codigo_barras": row[5],
        "quantidade_estoque": row[6],
        "receita_obrigatoria": row[7],
    }
    
    
    
#   BUSCAR MEDICAMENTO POR NOME

@router.get("/buscar/", response_model=list[MedicamentoResponse])
def buscar_medicamento_por_nome(nome: str):
    """
    Busca medicamentos cujo nome contém o texto informado (case-insensitive).
    Retorna lista de correspondências.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    
    cur.execute("""
        SELECT id, nome, lote, validade, quantidade_minima, codigo_barras,
               quantidade_estoque, receita_obrigatoria
        FROM medicamentos
        WHERE nome ILIKE %s;
    """, (f"%{nome}%",))

    rows = cur.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Nenhum medicamento encontrado com esse nome")

    medicamentos = []
    for row in rows:
        medicamentos.append({
            "id": row[0],
            "nome": row[1],
            "lote": row[2],
            "validade": row[3],
            "quantidade_minima": row[4],
            "codigo_barras": row[5],
            "quantidade_estoque": row[6],
            "receita_obrigatoria": row[7],
        })

    return medicamentos




#   CRIAR MEDICAMENTO

@router.post("/", response_model=MedicamentoResponse)
def criar_medicamento(medicamento: MedicamentoCreate):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO medicamentos
        (nome, lote, validade, quantidade_minima, codigo_barras,
         quantidade_estoque, receita_obrigatoria)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        medicamento.nome,
        medicamento.lote,
        medicamento.validade,
        medicamento.quantidade_minima,
        medicamento.codigo_barras,
        medicamento.quantidade_estoque,
        medicamento.receita_obrigatoria
    ))

    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return { "id": new_id, **medicamento.dict() }



#   ATUALIZAR PARCIAL 

@router.put("/{id}", response_model=MedicamentoResponse)
def atualizar_medicamento(id: int, medicamento: MedicamentoUpdate):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM medicamentos WHERE id = %s;", (id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")

    dados = medicamento.dict(exclude_unset=True)

    if not dados:
        conn.close()
        raise HTTPException(status_code=400, detail="Nenhum campo enviado para atualização")

    campos = ", ".join(f"{col} = %s" for col in dados.keys())
    valores = list(dados.values())
    valores.append(id)

    query = f"UPDATE medicamentos SET {campos} WHERE id = %s;"
    cur.execute(query, valores)

    conn.commit()
    conn.close()

    return { "id": id, **dados }



#   DELETAR

@router.delete("/{id}")
def deletar_medicamento(id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM medicamentos WHERE id = %s;", (id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")

    cur.execute("DELETE FROM medicamentos WHERE id = %s;", (id,))
    conn.commit()
    conn.close()

    return { "mensagem": "Medicamento removido com sucesso" }



