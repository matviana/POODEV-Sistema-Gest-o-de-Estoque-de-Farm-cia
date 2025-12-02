import numpy as np
from sklearn.neural_network import MLPRegressor
import pickle
import os


class RedeNeuralDemanda:
    """
    Rede neural para previsão de demanda geral OU por medicamento.
    """

    def __init__(self, modelo_path="modelo_demanda.pkl"):
        self.modelo_path = modelo_path
        self.modelo = None

        # Carrega o modelo se já existir
        if os.path.exists(self.modelo_path):
            self._carregar_modelo()

    # UTILIDADES 

    def _carregar_modelo(self):
        with open(self.modelo_path, "rb") as f:
            self.modelo = pickle.load(f)

    def _salvar_modelo(self):
        with open(self.modelo_path, "wb") as f:
            pickle.dump(self.modelo, f)

    # TREINAMENTO GERAL

    def treinar_com_eventos(self, vendas_mensais, eventos_mensais):
        """
        Treinamento geral (farmácia inteira).
        """
        if len(vendas_mensais) < 12 or len(eventos_mensais) < 12:
            raise Exception("São necessários 12 valores de vendas e 12 de eventos.")

        X = []
        y = []

        for i in range(len(vendas_mensais) - 3):
            ultimos_3 = vendas_mensais[i:i + 3]
            indice_mes_previsto = (i + 3) % 12
            mes_normalizado = (indice_mes_previsto + 1) / 12
            evento = eventos_mensais[indice_mes_previsto]

            entrada = ultimos_3 + [mes_normalizado, evento]
            X.append(entrada)
            y.append(vendas_mensais[i + 3])

        X = np.array(X)
        y = np.array(y)

        self.modelo = MLPRegressor(
            hidden_layer_sizes=(64, 64),
            activation='relu',
            solver='adam',
            max_iter=4000,
            random_state=42
        )

        self.modelo.fit(X, y)
        self._salvar_modelo()

    # PREVISÃO GERAL 

    def prever_proximo_mes_eventos(self, ultimos_3_meses, mes_atual, intensidade_evento):
        if self.modelo is None:
            raise Exception("O modelo geral ainda não foi treinado!")

        mes_normalizado = mes_atual / 12
        entrada = ultimos_3_meses + [mes_normalizado, intensidade_evento]

        pred = self.modelo.predict([entrada])[0]
        return max(pred, 0)

   #TREINAMENTO POR MEDICAMENTO 

    @staticmethod
    def get_model_path(nome_medicamento):
        nome_limpo = nome_medicamento.lower().replace(" ", "_")
        pasta = "modelos_medicamentos"
        os.makedirs(pasta, exist_ok=True)
        return f"{pasta}/{nome_limpo}.pkl"

    @classmethod
    def treinar_medicamento(cls, nome_medicamento, vendas_mensais, eventos_mensais):
        modelo_path = cls.get_model_path(nome_medicamento)
        instancia = cls(modelo_path)

        instancia.treinar_com_eventos(vendas_mensais, eventos_mensais)
        return True

    @classmethod
    def prever_medicamento(cls, nome_medicamento, ultimos_3_meses, mes_atual, intensidade_evento):
        modelo_path = cls.get_model_path(nome_medicamento)

        if not os.path.exists(modelo_path):
            raise Exception(f"Modelo do medicamento '{nome_medicamento}' ainda não foi treinado.")

        instancia = cls(modelo_path)
        return instancia.prever_proximo_mes_eventos(
            ultimos_3_meses,
            mes_atual,
            intensidade_evento
        )
