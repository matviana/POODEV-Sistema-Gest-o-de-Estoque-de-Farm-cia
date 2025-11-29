import numpy as np
from sklearn.neural_network import MLPRegressor
import pickle
import os
from datetime import datetime


class RedeNeuralDemanda:
    """
    Rede neural simples para previsão de demanda futura.
    Critério 1: Histórico de vendas mensais.
    Critério 2: Sazonalidade (mês do ano).
    Critério 3: Eventos epidemiológicos (surtos, epidemias e pandemias).
    """

    def __init__(self, modelo_path="modelo_demanda.pkl"):
        self.modelo_path = modelo_path
        self.modelo = None

        
        if os.path.exists(self.modelo_path):
            self._carregar_modelo()

    def _carregar_modelo(self):
        with open(self.modelo_path, "rb") as f:
            self.modelo = pickle.load(f)

    def _salvar_modelo(self):
        with open(self.modelo_path, "wb") as f:
            pickle.dump(self.modelo, f)

    
    # TREINAMENTO COM SAZONALIDADE + EVENTOS EPIDEMIOLÓGICOS
    
    def treinar_com_eventos(self, vendas_mensais, eventos_mensais):
        """
        Treina a rede considerando:
        - histórico dos últimos 3 meses
        - mês do ano (sazonalidade)
        - intensidade de eventos epidemiológicos (0 a 1)

        vendas_mensais: lista de 12 valores (jan → dez)
        eventos_mensais: lista de valores entre 0 e 1
        """

        if len(vendas_mensais) < 12 or len(eventos_mensais) < 12:
            raise Exception("São necessários 12 valores de vendas e 12 valores de eventos.")

        X = []
        y = []

        for i in range(len(vendas_mensais) - 3):
            ultimos_3 = vendas_mensais[i:i+3]

            # Índice do mês que será previsto (0 a 11)
            indice_mes_previsto = (i + 3) % 12

            # Normalização do mês
            mes_normalizado = (indice_mes_previsto + 1) / 12

            # Intensidade do evento epidemiológico (0 a 1)
            evento = eventos_mensais[indice_mes_previsto]

            # Entrada completa
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

        print("Modelo treinado com histórico + sazonalidade + eventos epidemiológicos.")

    
    # PREVISÃO COM SAZONALIDADE + EVENTOS EPIDEMIOLÓGICOS
    
    def prever_proximo_mes_eventos(self, ultimos_3_meses, mes_atual, intensidade_evento):
        """
        ultimos_3_meses: [v1, v2, v3]
        mes_atual: mês desejado (1 a 12)
        intensidade_evento: 0 a 1
        """

        if self.modelo is None:
            raise Exception("ERRO: o modelo ainda não foi treinado!")

        mes_normalizado = mes_atual / 12

        entrada = ultimos_3_meses + [mes_normalizado, intensidade_evento]

        X = np.array([entrada])
        pred = self.modelo.predict(X)[0]

        return max(pred, 0)

