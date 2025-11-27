import numpy as np
from sklearn.neural_network import MLPRegressor
import pickle
import os


class RedeNeuralDemanda:
    """
    Rede neural simples para previsão de demanda futura.
    Etapa 1: Apenas histórico de vendas mensais.
    """

    def __init__(self, modelo_path="modelo_demanda.pkl"):
        self.modelo_path = modelo_path
        self.modelo = None

        # Se já existir modelo treinado, carregue.
        if os.path.exists(self.modelo_path):
            self._carregar_modelo()

    def _carregar_modelo(self):
        with open(self.modelo_path, "rb") as f:
            self.modelo = pickle.load(f)

    def _salvar_modelo(self):
        with open(self.modelo_path, "wb") as f:
            pickle.dump(self.modelo, f)

    def treinar_historico(self, vendas_mensais):
        """
        Treina a rede neural apenas com histórico de vendas mensais.
        vendas_mensais = [12 valores] por exemplo.
        """

        # Transformar em formato de treino:
        # Ex: usar janelas de 3 meses → prever o próximo mês.
        X = []
        y = []

        # Exemplo: (jan, fev, mar) → prever abril
        for i in range(len(vendas_mensais) - 3):
            X.append(vendas_mensais[i:i+3])
            y.append(vendas_mensais[i+3])

        X = np.array(X)
        y = np.array(y)

        # Criando modelo MLP
        self.modelo = MLPRegressor(
            hidden_layer_sizes=(16, 16),
            activation='relu',
            solver='adam',
            max_iter=2000,
            random_state=42
        )

        self.modelo.fit(X, y)
        self._salvar_modelo()
        print("Modelo treinado e salvo com sucesso usando apenas histórico de vendas.")

    def prever_proximo_mes(self, ultimos_3_meses):
        """
        Recebe: [v1, v2, v3]
        Retorna previsão do próximo mês.
        """

        if self.modelo is None:
            raise Exception("ERRO: o modelo ainda não foi treinado!")

        X = np.array([ultimos_3_meses])
        pred = self.modelo.predict(X)[0]
        return max(pred, 0)  # evitar valores negativos

