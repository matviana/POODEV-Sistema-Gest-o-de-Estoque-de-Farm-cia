// Alternar abas
function abrirAba(nome) {
    document.querySelectorAll(".aba").forEach(div => div.style.display = "none");
    document.getElementById(nome).style.display = "block";
}

// Consultar movimentações
async function consultarMovimentacoes() {
    const tipo = document.getElementById("tipo").value;
    const codigo = document.getElementById("codigo_barras").value;

    let url = "/historico/movimentacoes?limite=200";

    if (tipo) url += `&tipo=${tipo}`;
    if (codigo) url += `&codigo_barras=${codigo}`;

    const resp = await fetch(url);
    const data = await resp.json();

    const tabela = document.getElementById("tabela_movimentacoes");
    tabela.innerHTML = "";

    data.movimentacoes.forEach(m => {
        tabela.innerHTML += `
            <tr>
                <td>${m.id}</td>
                <td>${m.codigo_barras}</td>
                <td>${m.nome}</td>
                <td>${m.tipo}</td>
                <td>${m.quantidade}</td>
                <td>${m.estoque_antes}</td>
                <td>${m.estoque_depois}</td>
                <td>${m.datahora}</td>
                <td>${m.observacao ?? ""}</td>
            </tr>
        `;
    });
}

// Medicamentos mais vendidos
async function consultarMaisVendidos() {
    let mes = document.getElementById("mes").value;
    let ano = document.getElementById("ano").value;

    let url = "/historico/mais_vendidos";

    if (mes) url += `?mes=${mes}`;
    if (mes && ano) url += `&ano=${ano}`;
    else if (!mes && ano) url += `?ano=${ano}`;

    const resp = await fetch(url);
    const data = await resp.json();

    const tabela = document.getElementById("tabela_vendidos");
    tabela.innerHTML = "";

    data.mais_vendidos.forEach(item => {
        tabela.innerHTML += `
            <tr>
                <td>${item.nome}</td>
                <td>${item.total_vendido}</td>
            </tr>
        `;
    });
}
