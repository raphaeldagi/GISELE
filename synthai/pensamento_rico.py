"""Pensamento rico (Parte 29, P353): o mesmo pensamento logístico, com mais pesos.

As Partes 24–25 acharam a raiz do "pensar melhor, decidir pior": o modelo logístico com 4 pesos (intercepto,
discordância, nota − melhor, leitura) é MAL ESPECIFICADO, e o ajuste exato erra justamente onde se decide. Aqui as três
variáveis entram também ao quadrado e em produtos dois a dois:

    x = (1, a, b, c, a², b², c², ab, ac, bc),   a = discordância, b = nota − melhor, c = leitura

São 1 + d + d(d+1)/2 = 1 + 3 + 6 = 10 pesos (d = 3). Mais pesos reduzem o erro de especificação e aumentam a variância:
com poucos eventos por peso (Peduzzi et al., 1996: abaixo de ~10, os coeficientes ficam instáveis), o ajuste pode piorar
fora da amostra. Por isso o ajuste é de Newton com uma penalidade ridge λ = 1 nos pesos (uma priori normal de variância 1),
sem Firth (com 10 pesos, a alavanca de Firth custaria ~100 operações por amostra)."""

from .pensamento_exato import PensamentoExato, ajustar_logistica


class PensamentoRico(PensamentoExato):
    def __init__(self, taxa=0.05, ridge=1.0):
        super().__init__(taxa, firth=False)
        self.w = [0.0] * 10
        self.ridge = ridge

    @staticmethod
    def _x(opcao, melhor, leitura):
        a, b, c = opcao.discordancia, opcao.comite - melhor, leitura
        return (1.0, a, b, c, a * a, b * b, c * c, a * b, a * c, b * c)

    def calibrar(self, historico, epocas=None):
        xs, ys = [], []
        for episodio in historico:
            melhor = max(o.comite for o, _, _ in episodio)
            for o, rotulo, leitura in episodio:
                xs.append(self._x(o, melhor, leitura))
                ys.append(1.0 if rotulo else 0.0)
        self.w = ajustar_logistica(xs, ys, firth=False, ridge=self.ridge)
