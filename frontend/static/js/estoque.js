function mostrarAba(id) {
    document.querySelectorAll(".aba").forEach(div => div.style.display = "none");
    document.getElementById(id).style.display = "block";
}

// ----------- ENTRADA DE ESTOQUE -----------
async function entradaEstoque() {
    const payload = {
        codigo_barras: document.getElementById("entrada_codigo").value,
        quantidade: parseInt(document.getElementById("entrada_quantidade").value),
        observacao: document.getElementById("entrada_obs").value
    };

    const r = await fetch("/estoque/entrada", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    document.getElementById("resultado_entrada").textContent = await r.text();
}

// ----------- SAÍDA DE ESTOQUE -----------
async function saidaEstoque() {
    const payload = {
        codigo_barras: document.getElementById("saida_codigo").value,
        quantidade: parseInt(document.getElementById("saida_quantidade").value),
        observacao: document.getElementById("saida_obs").value,
        caminho_receita: document.getElementById("saida_receita").value
    };

    const r = await fetch("/estoque/saida", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    document.getElementById("resultado_saida").textContent = await r.text();
}

// ----------- ALERTAS -----------
async function buscarAlertas() {
    const r = await fetch("/estoque/alertas");
    document.getElementById("resultado_alertas").textContent = await r.text();
}

// ----------- ESTOQUE BAIXO -----------
async function buscarEstoqueBaixo() {
    const threshold = document.getElementById("baixo_threshold").value;
    const pct = document.getElementById("baixo_pct").value;

    let url = "/estoque/baixo?";
    if (threshold) url += `threshold=${threshold}&`;
    if (pct) url += `porcentagem=${pct}&`;

    const r = await fetch(url);
    document.getElementById("resultado_baixo").textContent = await r.text();
}

// ----------- REPOSIÇÃO AUTOMÁTICA -----------
async function reporAutomatico() {
    const r = await fetch("/estoque/repor_automatico", {
        method: "POST"
    });

    document.getElementById("resultado_repor").textContent = await r.text();
}
