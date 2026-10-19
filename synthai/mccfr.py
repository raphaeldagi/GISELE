"""MCCFR com amostragem do ACASO (chance-sampled CFR; Zinkevich et al. 2007, Lanctot et al. 2009) no pôquer de Kuhn (Parte 118). Biblioteca padrão.

O CFR vanilla da Parte 113 percorre, a cada iteração, as 6 distribuições de cartas. Aqui cada iteração SORTEIA uma distribuição (o acaso dado de
fora, por um LCG inteiro, como na rodada 65) e atualiza só a árvore dela. É o passo mínimo rumo a jogos em que não dá para enumerar o acaso
(o Leduc tem 120 distribuições, o pôquer real, bilhões): custa 1/6 da iteração vanilla, e paga com ruído de amostragem."""

from synthai.cfr import CFR, DISTRIBUICOES


class LCG:
    """O acaso dado de fora, portável entre línguas (o mesmo LCG da rodada 84)."""

    def __init__(self, semente):
        self.x = semente

    def proximo(self, n):
        self.x = (1103515245 * self.x + 12345) % 2147483648
        return (self.x >> 16) % n


class CFRAcaso(CFR):
    """O CFR da Parte 113 com o acaso amostrado: o mesmo _cfr numa distribuição sorteada por iteração."""

    def iterar_amostrado(self, n, semente):
        g = LCG(semente)
        for _ in range(n):
            c1, c2 = DISTRIBUICOES[g.proximo(6)]
            self._cfr(c1, c2, "", 1.0, 1.0)
        return self


def explorabilidade_amostrada(iteracoes, semente):
    from synthai.cfr import explorabilidade
    return explorabilidade(CFRAcaso().iterar_amostrado(iteracoes, semente).media())
