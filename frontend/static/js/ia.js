const API = "http://127.0.0.1:8000/ia";

function show(data) {
    document.getElementById("resultado").textContent =
        JSON.stringify(data, null, 2);
}

// ------------------ MODELO GERAL ------------------ //

async function treinarGeral() {
    const vendas = document.getElementById("vendas_geral").value.split(",").map(Number);
    const eventos = document.getElementById("eventos_geral").value.split(",").map(Number);

    const resp = await fetch(`${API}/treinar`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            vendas_mensais: vendas,
            eventos_mensais: eventos
        })
    });

    show(await resp.json());
}

async function preverGeral() {
    const ultimos3 = document.getElementById("ultimos3_geral").value.split(",").map(Number);
    const mes = Number(document.getElementById("mes_atual_geral").value);
    const evento = Number(document.getElementById("evento_geral").value);

    const resp = await fetch(`${API}/prever_demanda`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            ultimos_3_meses: ultimos3,
            mes_atual: mes,
            intensidade_evento: evento
        })
    });

    show(await resp.json());
}

// ------------------ POR MEDICAMENTO ------------------ //

async function treinarMedicamento() {
    const nome = document.getElementById("nome_med_treinar").value;
    const vendas = document.getElementById("vendas_med").value.split(",").map(Number);
    const eventos = document.getElementById("eventos_med").value.split(",").map(Number);

    const resp = await fetch(`${API}/treinar_medicamento`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            nome_medicamento: nome,
            vendas_mensais: vendas,
            eventos_mensais: eventos
        })
    });

    show(await resp.json());
}

async function preverMedicamento() {
    const nome = document.getElementById("nome_med_prever").value;
    const ultimos3 = document.getElementById("ultimos3_med").value.split(",").map(Number);
    const mes = Number(document.getElementById("mes_atual_med").value);
    const evento = Number(document.getElementById("evento_med").value);

    const resp = await fetch(`${API}/prever_medicamento`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            nome_medicamento: nome,
            ultimos_3_meses: ultimos3,
            mes_atual: mes,
            intensidade_evento: evento
        })
    });

    show(await resp.json());
}
