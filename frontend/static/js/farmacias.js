const API = "http://127.0.0.1:8000";

async function cadastrarFarmacia() {
    const nome = document.getElementById("nomeFarmacia").value;
    const endereco = document.getElementById("enderecoFarmacia").value;
    const telefone = document.getElementById("telefoneFarmacia").value;
    const cnpj = document.getElementById("cnpjFarmacia").value;

    const data = { nome, endereco, telefone, cnpj };

    const resp = await fetch("http://127.0.0.1:8000/farmacias/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const resposta = await resp.json();
    document.getElementById("resultadoCadastro").textContent =
        JSON.stringify(resposta, null, 4);
}

// Listar todas farmácias
async function listarFarmacias() {
    const resp = await fetch(`${API}/farmacias/`);
    const dados = await resp.json();

    document.getElementById("resultadoLista").textContent =
        JSON.stringify(dados, null, 4);
}

// Buscar por ID
async function buscarFarmacia() {
    const id = document.getElementById("buscarId").value;

    const resp = await fetch(`${API}/farmacias/${id}`);
    const dados = await resp.json();

    document.getElementById("resultadoBusca").textContent =
        JSON.stringify(dados, null, 4);
}

// Deletar farmácia
async function deletarFarmacia() {
    const id = document.getElementById("deleteId").value;

    const resp = await fetch(`${API}/farmacias/${id}`, {
        method: "DELETE"
    });

    const dados = await resp.json();

    document.getElementById("resultadoDelete").textContent =
        JSON.stringify(dados, null, 4);
}
