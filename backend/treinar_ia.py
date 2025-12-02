from backend.redeneural import RedeNeuralDemanda

vendas = [120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230]
eventos = [0.1, 0.3, 0.0, 0.2, 0.6, 0.8, 0.4, 0.1, 0.0, 0.7, 0.2, 0.3]

ia = RedeNeuralDemanda()
ia.treinar_com_eventos(vendas, eventos)

print("Treinamento concluído!")
