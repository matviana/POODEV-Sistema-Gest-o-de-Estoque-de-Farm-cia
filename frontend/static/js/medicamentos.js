const API = "http://127.0.0.1:8000";

async function cadastrarMedicamento() {
    const data = {
        nome: document.getElementById("nome").value,
        lote: document.getElementById("lote").value,
        validade: document.getElementById("validade").value,
        quantidade_minima: parseInt(document.getElementById("quantidade_minima").value),
        codigo_barras: document.getElementById("codigo_barras").value,
        quantidade_estoque: parseInt(document.getElementById("quantidade_estoque").value),
        receita_obrigatoria: document.getElementById("receita_obrigatoria").checked
    };

    const resp = await fetch(`${API}/medicamentos/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const resultado = await resp.json();
    document.getElementById("resultadoCadastro").textContent =
        JSON.stringify(resultado, null, 4);
}

// Listar todos medicamentos
async function listarTodos() {
    const resp = await fetch(`${API}/medicamentos/`);
    const dados = await resp.json();
    document.getElementById("resultadoTodos").textContent = JSON.stringify(dados, null, 4);
}

async function buscarPorNome() {
    const nome = document.getElementById("buscarNome").value;

    const resp = await fetch(`${API}/medicamentos/buscar/?nome=${nome}`);
    const dados = await resp.json();

    document.getElementById("resultadoNome").textContent =
        JSON.stringify(dados, null, 4);
}


// Deletar medicamento
async function deletarMedicamento() {
    const id = document.getElementById("deleteId").value;

    const resp = await fetch(`${API}/medicamentos/${id}`, {
        method: "DELETE"
    });

    if (resp.status === 200) {
        document.getElementById("resultadoDelete").textContent = "Deletado com sucesso";
    } else {
        document.getElementById("resultadoDelete").textContent = "Erro ao deletar";
    }
}