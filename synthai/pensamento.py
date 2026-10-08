"""Pensamento (P43, P83, P145): a probabilidade calibrada de uma opção ser catastrófica.

Regressão logística sobre (1, discordância, nota do comitê − melhor nota, leitura do sensor). Calibrada com um
histórico auditado e, depois, só com o resultado das próprias escolhas (a "sombra própria" da Parte 6)."""

from math import exp


class Pensamento:
    def __init__(self, taxa=0.05):
        self.w = [0.0, 0.0, 0.0, 0.0]
        self.taxa = taxa

    @staticmethod
    def _x(opcao, melhor, leitura):
        return (1.0, opcao.discordancia, opcao.comite - melhor, leitura)

    def p_catastrofe(self, opcao, melhor, leitura=0.0):
        z = sum(wi * xi for wi, xi in zip(self.w, self._x(opcao, melhor, leitura)))
        return 1 / (1 + exp(-max(-30.0, min(30.0, z))))

    def aprender(self, opcao, melhor, leitura, rotulo):
        erro = self.p_catastrofe(opcao, melhor, leitura) - rotulo
        self.w = [wi - self.taxa * erro * xi for wi, xi in zip(self.w, self._x(opcao, melhor, leitura))]

    def calibrar(self, historico, epocas=3):
        for _ in range(epocas):
            for episodio in historico:
                melhor = max(o.comite for o, _, _ in episodio)
                for o, rotulo, leitura in episodio:
                    self.aprender(o, melhor, leitura, rotulo)
