from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa o router de medicamentos
from backend.routers.medicamentos_router import router as medicamentos_router


app = FastAPI(
    title="API - Sistema de Estoque da Farmácia",
    description="API que integra o backend em Python com o frontend em React",
    version="1.0.0"
)

# ================================
# CONFIGURAÇÃO DE CORS
# ================================
# Permite o frontend React acessar esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois podemos restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# ROTAS DA API
# ================================
@app.get("/")
def raiz():
    return {"status": "online", "mensagem": "API da Farmácia funcionando!"}

# Registro do router de medicamentos
app.include_router(
    medicamentos_router,
    prefix="/medicamentos",
    tags=["Medicamentos"]
)

