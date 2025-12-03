from backend.redeneural import RedeNeuralDemanda

vendas = [150,160,170,180,190,200,210,220,800,230,240,250]
eventos = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.9, 0.1, 0.1, 0.1]

ia = RedeNeuralDemanda()
ia.treinar_com_eventos(vendas, eventos)

print("Treinamento feito")
